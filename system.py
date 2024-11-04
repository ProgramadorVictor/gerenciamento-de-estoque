class Produto:
    #Criação da classe 'Produto', está classe deve armazenar as informações relacionadas ao produto. As informações estão sendo passados por parâmetros.
    def __init__(self, nome, categoria, quantidade, preco, localizacao):
        self.nome = nome #Atribuindo o nome
        self.categoria = categoria #Atribuindo a categoria
        self.quantidade = quantidade #Atribuindo a quantidade
        self.preco = preco #Atribuindo o preço
        self.localizacao = localizacao #Atribuindo a localização
    #As informações são recebidas pelo construtor e armazenadas posteriormente pelos atributos da classe

def menu():
    print("0 - Gerente")
    print("1 - Estoquista")
    print("2 - Usuário")

def main():
    while True:
        menu()
        escolha = input("Digite o número da sua escolha (0, 1 ou 2): ")

        if escolha == '0':
            print("Você selecionou: Gerente")
            break
        elif escolha == '1':
            print("Você selecionou: Estoquista")
            break
        elif escolha == '2':
            print("Você selecionou: Usuário")
            break
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()
