import sqlite3
import datetime
#Comandos sqlite para não esquecer.
# sqlite3 estoque.db
# .tables, select * from produtos, .exit

#As tabelas foram criadas usando o padrão do Laravel um framework php, eu gosto desse padrão, portanto preferir utilizar.

class Produto:
    #Criação da classe 'Produto', está classe deve armazenar as informações relacionadas ao produto. As informações estão sendo passados por parâmetros.
    def __init__(self, nome, categoria, quantidade, preco, localizacao):
        self.nome = nome #Atribuindo o nome
        self.categoria = categoria #Atribuindo a categoria
        self.quantidade = quantidade #Atribuindo a quantidade
        self.preco = preco #Atribuindo o preço
        self.localizacao = localizacao #Atribuindo a localização
    #As informações são recebidas pelo construtor e armazenadas posteriormente pelos atributos da classe

def criar_banco():
    conn = sqlite3.connect('estoque.db')# Cria o banco de dados.
    cursor = conn.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            localizacao TEXT NOT NULL
        )
    ''') #Criação da tabela produtos

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''') #Criação de tabela para solicitações de usuários.

    conn.commit() #Faz o commit das mudançãs
    conn.close() #Fecha a conexão

def adicionar_produto(produto):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO produtos (nome, categoria, quantidade, preco, localizacao)
        VALUES (?, ?, ?, ?, ?)
    ''', (produto.nome, produto.categoria, produto.quantidade, produto.preco, produto.localizacao)) #Inserindo os valores

    conn.commit()
    conn.close()

def solicitar_compra(produto_id, quantidade): #Solicitar compras, somente para usuários.
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Verifica se o produto_id existe na tabela de produtos
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    
    if produto is None:
        print("Produto não encontrado. Solicitação de compra não pode ser realizada.")
    else:
        cursor.execute('''
            INSERT INTO solicitacoes (produto_id, quantidade, data)
            VALUES (?, ?, ?)
        ''', (produto_id, quantidade, datetime.datetime.now().isoformat())) # Se o produto existe, registra a solicitação.

        conn.commit()
        print("Solicitação de compra enviada com sucesso!")
    conn.close()

def emitir_relatorio(): #Função para emitir relatório
    print('')

def menu_funcao():
    print("0 - Gerente")
    print("1 - Estoquista")
    print("2 - Usuário")

def menu_estoquista():
    print("Estoquista. Por favor, selecione uma opção:")
    print("1 - Adicionar Produto")
    print("2 - Voltar ao Menu Principal")

def menu_usuario():
    print("Usuário, Por favor. Selecione uma opção:")
    print("1 - Solicitar Compra de Produto")
    print("2 - Emitir Relatório Semanal")
    print("3 - Voltar ao Menu Principal")

def main():
    criar_banco() #Cria o banco de dados juntamente com a tabela.
    while True:
        menu_funcao()
        escolha = input("Digite o número da sua escolha (0, 1 ou 2): ")

        if escolha == '0':
            print("Você selecionou: Gerente")
            break
        elif escolha == '1':
            print("Você selecionou: Estoquista")
            while True:
                menu_estoquista()
                operacao = input("Digite o número da sua opção: ")
                if operacao == '1': # Adicionar um produto
                    nome = input("Digite o nome do produto: ")
                    categoria = input("Digite a categoria do produto: ")
                    quantidade = int(input("Digite a quantidade do produto: "))
                    preco = float(input("Digite o preço do produto: "))
                    localizacao = input("Digite a localização do produto: ")

                    produto = Produto(nome, categoria, quantidade, preco, localizacao)
                    adicionar_produto(produto)
                    print("Produto adicionado com sucesso!")
                elif operacao == '2': # Voltar para o menu principal
                    break
        elif escolha == '2':
            print("Você selecionou: Usuário")
            while True:
                menu_usuario()
                operacao = input("Digite o número da sua opção: ")
                if operacao == '1': # Solicitar compra de produto
                    produto_id = int(input("Digite o ID do produto: "))
                    quantidade = int(input("Digite a quantidade a ser solicitada: "))
                    solicitar_compra(produto_id, quantidade)
                elif operacao == '2': # Emitir relatório semanal
                    emitir_relatorio()
                elif operacao == '3': # Voltar para o menu principal
                    break
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()
