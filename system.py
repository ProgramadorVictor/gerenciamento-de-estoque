class Produto:
    #Criação da classe 'Produto', está classe deve armazenar as informações relacionadas ao produto. As informações estão sendo passados por parâmetros.
    def __init__(self, nome, categoria, quantidade, preco, localizacao):
        self.nome = nome #Atribuindo o nome
        self.categoria = categoria #Atribuindo a categoria
        self.quantidade = quantidade #Atribuindo a quantidade
        self.preco = preco #Atribuindo o preço
        self.localizacao = localizacao #Atribuindo a localização
    #As informações são recebidas pelo construtor e armazenadas posteriormente pelos atributos da classe