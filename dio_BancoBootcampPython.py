print("=" * 40)
print("     Bem-vindo ao Banco PythonBank")
print("=" * 40)

saldo = 0.0
limite_saque = 500
saques_diarios = 3
extrato = ""

while True:
    print("\nEscolha uma das opções abaixo:")
    print("[d] Depósito")
    print("[s] Saque")
    print("[e] Extrato")
    print("[q] Sair")

    opcao = input("Opção: ").lower()

    if opcao == "d":
        valor = float(input("Valor do depósito: R$ "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:,.2f}\n"
        else:
            print("Valor inválido para depósito!")

    elif opcao == "s":
        if saques_diarios == 0:
            print("Limite de saques diários atingido!")
            continue

        valor = float(input("Valor do saque: R$ "))
        if valor > limite_saque:
            print("Limite por saque é de R$ 500,00!")
        elif valor > saldo:
            print("Saldo insuficiente!")
        elif valor > 0:
            saldo -= valor
            saques_diarios -= 1
            extrato += f"Saque:    R$ {valor:,.2f}\n"
        else:
            print("Valor inválido para saque!")

    elif opcao == "e":
        print("\n===== EXTRATO =====")
        print(extrato if extrato else "Não foram realizadas movimentações.")
        print(f"Saldo atual: R$ {saldo:,.2f}")
        print("===================")

    elif opcao == "q":
        print("Saindo... Obrigado por usar o PythonBank!")
        break

    else:
        print("Opção inválida! Tente novamente.")
