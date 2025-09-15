# =========================
# Instalação de pacotes
# =========================
# Rode no terminal (VS Code/Colab):
# pip install langchain langchain-community langchain-huggingface \
# transformers accelerate bitsandbytes sentence-transformers \
# faiss-cpu langchain-text-splitters pymupdf pydantic

# =========================
# Imports
# =========================
from pathlib import Path
import re
from typing import List, Dict, Literal
from pydantic import BaseModel, Field

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

from transformers import pipeline

# =========================
# Modelos (Open Source)
# =========================
# LLM principal para respostas (Mistral)
llm = HuggingFacePipeline.from_model_id(
    model_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    model_kwargs={"temperature": 0.7, "max_new_tokens": 512}
)

# Modelo de triagem (classificação simples)
classifier = pipeline("text-classification", model="facebook/bart-large-mnli")

# =========================
# Prompt de triagem
# =========================
TRIAGEM_PROMPT = """
Você é um triador de Service Desk para políticas internas da empresa Carraro Desenvolvimento.
Sua função é classificar a mensagem do usuário em:
- AUTO_RESOLVER: Perguntas claras sobre regras ou procedimentos descritos nas políticas.
- PEDIR_INFO: Mensagens vagas ou que faltam informações.
- ABRIR_CHAMADO: Pedidos de exceção ou acesso especial.

Além disso, classifique a urgência: BAIXA, MEDIA ou ALTA.
Retorne SOMENTE JSON no formato:
{
  "decisao": "...",
  "urgencia": "...",
  "campos_faltantes": []
}
"""

class TriagemOut(BaseModel):
    decisao: Literal["AUTO_RESOLVER", "PEDIR_INFO", "ABRIR_CHAMADO"]
    urgencia: Literal["BAIXA", "MEDIA", "ALTA"]
    campos_faltantes: List[str] = Field(default_factory=list)

def triagem(mensagem: str) -> Dict:
    # Heurística básica usando classifier
    result = classifier(mensagem, candidate_labels=["AUTO_RESOLVER", "PEDIR_INFO", "ABRIR_CHAMADO"])
    decisao = max(result, key=lambda x: x["score"])["label"]

    urgencia = "BAIXA"
    if any(w in mensagem.lower() for w in ["urgente", "agora", "imediato", "crítico"]):
        urgencia = "ALTA"
    elif any(w in mensagem.lower() for w in ["preciso", "logo", "rápido"]):
        urgencia = "MEDIA"

    return TriagemOut(decisao=decisao, urgencia=urgencia, campos_faltantes=[]).model_dump()

# =========================
# Teste triagem
# =========================
testes_triagem = [
    "Posso reembolsar a internet?",
    "Quero mais 5 dias de trabalho remoto. Como faço?",
    "Posso reembolsar cursos ou treinamentos da DIO?",
    "Quantas capivaras tem no Rio Pinheiros?"
]

for msg in testes_triagem:
    print(f"Pergunta: {msg}\n -> Resposta: {triagem(msg)}\n")

# =========================
# Carregamento de PDFs
# =========================
docs = []
pdf_path = Path("./pdfs/")  # Coloque seus PDFs aqui
for n in pdf_path.glob("*.pdf"):
    try:
        loader = PyMuPDFLoader(str(n))
        docs.extend(loader.load())
        print(f"Carregado com sucesso: {n.name}")
    except Exception as e:
        print(f"Erro ao carregar {n.name}: {e}")

print(f"Total de documentos carregados: {len(docs)}")

# =========================
# Split de documentos
# =========================
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
chunks = splitter.split_documents(docs)

# =========================
# Embeddings e FAISS
# =========================
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embeddings)

retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.3, "k": 4}
)

# =========================
# RAG: Perguntas sobre políticas
# =========================
prompt_rag = ChatPromptTemplate.from_messages([
    ("system",
     "Você é um Assistente de Políticas Internas (RH/IT). "
     "Responda SOMENTE com base no contexto fornecido. "
     "Se não houver base suficiente, responda apenas 'Não sei'."),
    ("human", "Pergunta: {input}\n\nContexto:\n{context}")
])

document_chain = create_stuff_documents_chain(llm, prompt_rag)

# =========================
# Funções auxiliares
# =========================
def _clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()

def extrair_trecho(texto: str, query: str, janela: int = 240) -> str:
    txt = _clean_text(texto)
    termos = [t.lower() for t in re.findall(r"\w+", query or "") if len(t) >= 4]
    pos = -1
    for t in termos:
        pos = txt.lower().find(t)
        if pos != -1: break
    if pos == -1: pos = 0
    ini, fim = max(0, pos - janela//2), min(len(txt), pos + janela//2)
    return txt[ini:fim]

def formatar_citacoes(docs_rel: List, query: str) -> List[Dict]:
    cites, seen = [], set()
    for d in docs_rel:
        src = Path(d.metadata.get("source", "")).name
        page = int(d.metadata.get("page", 0)) + 1
        key = (src, page)
        if key in seen:
            continue
        seen.add(key)
        cites.append({
            "documento": src,
            "pagina": page,
            "trecho": extrair_trecho(d.page_content, query)
        })
    return cites[:3]

def perguntar_politica_RAG(pergunta: str) -> Dict:
    docs_relacionados = retriever.invoke(pergunta)

    if not docs_relacionados:
        return {"answer": "Não sei.", "citacoes": [], "contexto_encontrado": False}

    answer = document_chain.invoke({"input": pergunta, "context": docs_relacionados})
    txt = (answer or "").strip()

    if txt.rstrip(".!?") == "Não sei":
        return {"answer": "Não sei.", "citacoes": [], "contexto_encontrado": False}

    return {
        "answer": txt,
        "citacoes": formatar_citacoes(docs_relacionados, pergunta),
        "contexto_encontrado": True
    }

# =========================
# Teste RAG
# =========================
testes_rag = [
    "Posso reembolsar a internet?",
    "Quero mais 5 dias de trabalho remoto. Como faço?",
    "Posso reembolsar cursos ou treinamentos da Alura?",
    "Quantas capivaras tem no Rio Pinheiros?"
]

for msg in testes_rag:
    resposta = perguntar_politica_RAG(msg)
    print(f"\nPERGUNTA: {msg}")
    print(f"RESPOSTA: {resposta['answer']}")
    if resposta['contexto_encontrado']:
        print("CITAÇÕES:")
        for c in resposta['citacoes']:
            print(f" - Documento: {c['documento']}, Página: {c['pagina']}")
            print(f"   Trecho: {c['trecho']}")
        print("------------------------------------")
