dycar = {
    "toyota": {"modelo": "corolla", "preco": 100}, 
    "ford": {"modelo": "focus", "preco": 80},
    "chevrolet": {"modelo": "silverado", "preco": 570}
}

while True:
    try:
        print("Sistema de Con")
        escolha = int(input("\n1. Adicionar um Carro\n2. Ver Carros disponíveis\n3. Comprar Carro\n4. Sair\n\nEscolha: "))

        if escolha == 1:
            marca = input("Digite a marca do carro: ").lower()
            modelo = input("Digite o modelo do carro: ").lower()
            preco = int(input("Digite o preço do carro (em milhar): "))
            dycar[marca] = {"modelo": modelo, "preco": preco}
            print("Carro adicionado com sucesso!")

        elif escolha == 2:
            print("\nCarros disponíveis:")
            for marca, info in dycar.items():
                print(f"{marca} : {info['modelo']} - R${info['preco']} mil")

        elif escolha == 3:
            marca = input("Digite a marca do carro que deseja comprar: ").lower()
            if marca in dycar:
                confirmar = input(f"Você deseja comprar o {dycar[marca]['modelo']} por R${dycar[marca]['preco']} mil? (s/n): ").lower()
                if confirmar == "s":
                    print(f"Compra do {dycar[marca]['modelo']} realizada com sucesso!")
                    del dycar[marca]
                else:
                    print("Compra cancelada.")
            else:
                print("Marca não encontrada.")

        elif escolha == 4:
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")

    except ValueError:
        print("Digite um número válido.")