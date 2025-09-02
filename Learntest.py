import random

cartas = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
ordem_forca = cartas[:]  # cópia

def menu_principal():
    print('=' * 40)
    print('Bem-vindo ao LearnTest!'.center(40))
    print('=' * 40)

    while True:
        try:
            escolha = int(input('\nEscolha uma opção:\n[1] Estudar com Flashcards\n[2] Jogar Truco\nDigite: '))
            if escolha in [1, 2]:
                return escolha
            else:
                print("Digite apenas 1 ou 2.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def flashcards():
    print('\nModo Flashcards Ativado')
    prg1 = input('Digite sua Pergunta: ')
    rsp1 = input('Digite sua Resposta: ')
    print('\nSeu Flashcard:')
    print(f'Pergunta: {prg1}')
    print(f'Resposta: {rsp1}')

def proxima_manilha(carta):
    idx = ordem_forca.index(carta)
    return ordem_forca[(idx + 1) % len(ordem_forca)]

def gerar_forca_com_manilhas(vira):
    manilhas = [proxima_manilha(vira)]
    return {carta: (100 + i if carta in manilhas else i) for i, carta in enumerate(ordem_forca)}

def distribuir_mao(baralho):
    return [baralho.pop() for _ in range(3)]

def jogar_truco():
    print('\nTruco com manilha - Computador joga primeiro\n')

    baralho = cartas * 4
    random.shuffle(baralho)

    vira = baralho.pop()
    forca = gerar_forca_com_manilhas(vira)
    manilha = proxima_manilha(vira)

    print(f'Carta virada: {vira}  |  Manilha: {manilha}')

    jogador = distribuir_mao(baralho)
    computador = distribuir_mao(baralho)

    pontos_jogador = 0
    pontos_pc = 0

    for rodada in range(1, 4):
        print(f'\nRodada {rodada}')
        print('Suas cartas:', jogador)

        carta_pc = random.choice(computador)
        print(f'Computador jogou: {carta_pc}')
        computador.remove(carta_pc)

        escolha = input("Escolha uma carta (digite como aparece): ").upper()
        while escolha not in jogador:
            escolha = input("Carta inválida. Tente novamente: ").upper()
        jogador.remove(escolha)

        v_pc = forca[carta_pc]
        v_jog = forca[escolha]

        print(f'Você jogou: {escolha}')

        if v_pc > v_jog:
            print("Computador venceu a rodada.")
            pontos_pc += 1
        elif v_pc < v_jog:
            print("Você venceu a rodada.")
            pontos_jogador += 1
        else:
            print("Empate na rodada.")

        if pontos_jogador == 2 or pontos_pc == 2:
            break

    print('\nResultado Final:')
    if pontos_jogador > pontos_pc:
        print("Você venceu o jogo!")
    elif pontos_jogador < pontos_pc:
        print("O computador venceu o jogo.")
    else:
        print("Empate no jogo.")

def main():
    while True:
        opcao = menu_principal()

        if opcao == 1:
            flashcards()
        elif opcao == 2:
            jogar_truco()

        repetir = input('\nDeseja voltar ao menu? (s/n): ').lower()
        if repetir != 's':
            print('\nObrigado por usar o LearnTest. Até a próxima!')
            break

if __name__ == "__main__":
    main()
