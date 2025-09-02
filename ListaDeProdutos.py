print("Olá !! Bem Vindo a Loja De Produtos !\n Escolha Uma Opção Para Começar!")

estoque = {"arroz" : 20 ,"chinelo" : 10, "panela" : 110, "cadeira" : 50, "cola rato" : 15, "superbonder" : 2, "bonpátossi": 16}
esco = int(input("\n1- Ver Estoque\n2- Escolher Produto\n3- Sair\n : \n"))
while True :
    if esco == 1 :
        for item in estoque :
            print(item)
    
    elif esco == 2 :
        pro = input("Escolha Um Produto : ")
        print(f"R${estoque[pro]}")

    else :
        print("Cannot Error 404 !! Saindo Do Sistema... ")

    break