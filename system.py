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
            status TEXT DEFAULT 'pendente',
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

#As solicitações do usuario são definidas por 'pendente', 'aprovada' e 'negada'. Que são definidas posteriormentes pelo gerente da aplicação.
def solicitar_compra(produto_id, quantidade): #Solicitar compras, somente para usuários.
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Verifica se o produto_id existe na tabela de produtos
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    
    if produto is None: #Se o produto_id não existir.
        print("Produto não encontrado. Solicitação de compra não pode ser realizada.")
    else:
        estoque_disponivel = produto[3];
        if quantidade > estoque_disponivel: #Caso o usuario solicite mais do que tem ocorre um aviso e retornar a quantidade disponivel.
            print(f"Quantidades insuficiente no estoque. Disponivel no momento: {estoque_disponivel}.")
        else:
            cursor.execute('''
                INSERT INTO solicitacoes (produto_id, quantidade, data, status)
                VALUES (?, ?, ?, ?)
            ''', (produto_id, quantidade, datetime.datetime.now().isoformat(), 'pendente')) #Se o produto existe, registra a solicitação.

            conn.commit()
            print("Solicitação de compra enviada com sucesso!")
    conn.close()

def visualizar_solicitacoes_pendentes():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Exibe as solicitações pendentes
    cursor.execute("SELECT * FROM solicitacoes WHERE status = 'pendente'")
    solicitacoes = cursor.fetchall()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    if not solicitacoes: # Verifica se existe solicitações, se não existir, não mostra elas.
        print("Não há solicitações pendentes.")
    else:
        for solicitacao in solicitacoes:
            produto_id = solicitacao[1]
            quantidade = solicitacao[2]
            data = solicitacao[3]
            print(f"ID Solicitação: {solicitacao[0]} | Produto ID: {produto_id} | Quantidade: {quantidade} | Data: {data}")
        for produto in produtos: #Melhorando a visualização para saber qual produto esta relacionado.
            produto_id = produto[0]
            produto_nome = produto[1]
            quantidade = produto[3]
            print(f"Produto ID: {produto_id} | Nome do Produto: {produto_nome} | Quantidade: {quantidade}")

    conn.close()

def aprovar_rejeitar_solicitacao(id_solicitacao, aprovacao):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM solicitacoes WHERE id = ?', (id_solicitacao,)) # Verifica se a solicitação existe.
    solicitacao = cursor.fetchone()

    if solicitacao is None:
        print("Solicitação nao encontrada.")
    else:
        if aprovacao.lower() == 'aprovar':
            cursor.execute('SELECT * FROM produtos WHERE id = ?', (solicitacao[1],))
            produto = cursor.fetchone()
            quantidade_comprada = solicitacao[2]

            if produto:
                nova_quantidade = produto[3] - quantidade_comprada
                cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto[0]))
                print(f"Compra aprovada. Produto {produto[1]} (ID: {produto[0]}) quantidade atualizada.")

        cursor.execute('UPDATE solicitacoes SET status = ? WHERE id = ?', ('aprovada' if aprovacao.lower() == 'aprovar' else 'rejeitada', id_solicitacao))
        conn.commit()

    conn.close()

def produtos_para_usuario():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    #Exibe os produtos
    cursor.execute("SELECT id, nome, preco FROM produtos")    
    produtos = cursor.fetchall()

    for produto in produtos:
        nome = produto[1]; id_produto = produto[0]; preco = produto[2]
        print(f"Produto ID: {id_produto} | Nome do Produto: {nome} | Preço: {preco}")
    
    conn.close()

def emitir_relatorio(): #Função para emitir relatório
    print('')

def menu_funcao():
    print("0 - Gerente")
    print("1 - Estoquista")
    print("2 - Usuário")

def menu_estoquista():
    print("Estoquista. Por favor, selecione uma opção:")
    print("0 - Voltar ao Menu Principal")
    print("1 - Adicionar Produto")

def menu_usuario():
    print("Usuário, Por favor. Selecione uma opção:")
    print("0 - Voltar ao Menu Principal")
    print("1 - Solicitar Compra de Produto")
    print("2 - Emitir Relatório Semanal")
    print("3 - Listar os Produtos (Essa função não estava no trabalho. Mas é útil para visualizar os produtos disponiveis.)")

def menu_gerente():
    print("Gerente, por favor, selecione uma opção:")
    print("0 - Voltar ao Menu Principal")
    print("1 - Visualizar Solicitações Pendentes")
    print("2 - Aprovar/Rejeitar Solicitação")

def main():
    criar_banco() #Cria o banco de dados juntamente com a tabela.
    while True:
        menu_funcao()
        escolha = input("Digite o número da sua escolha (0, 1 ou 2): ")

        if escolha == '0':
            print("Você selecionou: Gerente")
            while True:
                menu_gerente()
                operacao = input("Digite o número da sua opção: ")
                if operacao == '0':
                    break
                elif operacao == '1': #Visualizar as solicitações de usuários pendentes
                    visualizar_solicitacoes_pendentes()
                elif operacao == '2': #Aprova ou rejeitar as solicitação.
                    id_solicitacao = int(input("Digite o ID da solicitação: "))
                    aprovacao = input("Digite 'aprovar' ou 'rejeitar': ")
                    aprovar_rejeitar_solicitacao(id_solicitacao, aprovacao)
        elif escolha == '1':
            print("Você selecionou: Estoquista")
            while True:
                menu_estoquista()
                operacao = input("Digite o número da sua opção: ")
                if operacao == '0':
                    break
                elif operacao == '1': # Adicionar um produto
                    nome = input("Digite o nome do produto: ")
                    categoria = input("Digite a categoria do produto: ")
                    quantidade = int(input("Digite a quantidade do produto: "))
                    preco = float(input("Digite o preço do produto: "))
                    localizacao = input("Digite a localização do produto: ")

                    produto = Produto(nome, categoria, quantidade, preco, localizacao)
                    adicionar_produto(produto)
                    print("Produto adicionado com sucesso!")
        elif escolha == '2':
            print("Você selecionou: Usuário")
            while True:
                menu_usuario()
                operacao = input("Digite o número da sua opção: ")
                if operacao == '0': # Voltar para o menu principal
                    break
                elif operacao == '1': # Solicitar compra de produto
                    produto_id = int(input("Digite o ID do produto: "))
                    quantidade = int(input("Digite a quantidade a ser solicitada: "))
                    solicitar_compra(produto_id, quantidade)
                elif operacao == '2': # Emitir relatório semanal
                    emitir_relatorio()
                elif operacao == '3': # Mostrar os produtos disponiveis
                    produtos_para_usuario()
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()
