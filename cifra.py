def cifra(texto):
    vogais = "aeiou"
    alfabeto = "abcdefghijklmnopqrstuvwxyz"

    resultado = []

    for ch in texto:
        if ch not in alfabeto:
            # Mantém espaços e pontuação
            resultado.append(ch)
        elif ch in vogais:
            resultado.append(ch)
        else:
            # Parte 1: consoante original
            resultado.append(ch)

            # Parte 2: vogal mais próxima
            pos = alfabeto.index(ch)
            menor_d = float('inf')
            escolha_v = None
            for v in vogais:
                d = abs(pos - alfabeto.index(v))
                if d < menor_d or (d == menor_d and v < escolha_v):
                    menor_d = d
                    escolha_v = v
            resultado.append(escolha_v)

            # Parte 3: próxima consoante
            prox = ch  # padrão: repetir a própria se for 'z'
            for nxt in alfabeto[pos+1:]:
                if nxt not in vogais:
                    prox = nxt
                    break
            resultado.append(prox)

    return "".join(resultado)

# Execução principal
if __name__ == "__main__":
    frase = input().strip().lower()  # aceita frases e converte para minúsculas
    print(cifra(frase))
