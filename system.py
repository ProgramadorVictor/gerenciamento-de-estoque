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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            descricao TEXT NOT NULL,
            data_registro TEXT NOT NULL
        )
    ''')

    conn.commit() #Faz o commit das mudançãs
    conn.close() #Fecha a conexão

def adicionar_produto(produto):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO produtos (nome, categoria, quantidade, preco, localizacao)
        VALUES (?, ?, ?, ?, ?)
    ''', (produto.nome, produto.categoria, produto.quantidade, produto.preco, produto.localizacao)) #Inserindo os valores

    descricao = f"Produto '{produto.nome}', Quantidade: {produto.quantidade}, Adicionado ao estoque."
    data_registro = datetime.datetime.now().isoformat()

    cursor.execute('''
        INSERT INTO registros (descricao, data_registro)
        VALUES (?, ?)
    ''', (descricao, data_registro))

    conn.commit()
    conn.close()

#As solicitações do usuario são definidas por 'pendente', 'aprovada' e 'negada'. Que são definidas posteriormentes pelo gerente da aplicação.
def solicitar_compra(): #Solicitar compras, somente para usuários.
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    produto_id = int(input("Digite o ID do produto: "))
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))  # Verifica se o produto_id existe na tabela de produtos
    produto = cursor.fetchone()

    if produto is None: #Se o produto_id não existir.
        print("Produto não encontrado. Solicitação de compra não pode ser realizada.")
        return
    
    quantidade = int(input("Digite a quantidade a ser solicitada: "))

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
def visualizar_todas_solicitacoes():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM solicitacoes")
    solicitacoes = cursor.fetchall()

    for solicitacao in solicitacoes:
        print(f"ID Solicitação: {solicitacao[0]} | Produto ID: {solicitacao[1]} | Quantidade: {solicitacao[2]} | Data: {solicitacao[3]} | Status: {solicitacao[4]}")
    conn.close()

def visualizar_solicitacoes_pendentes():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Exibe as solicitações pendentes
    cursor.execute("SELECT * FROM solicitacoes WHERE status = 'pendente'")
    solicitacoes = cursor.fetchall()

    if not solicitacoes: # Verifica se existe solicitações, se não existir, não mostra elas.
        print("Não há solicitações pendentes.")
        return False
    else:
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        for solicitacao in solicitacoes:
            produto_id = solicitacao[1]
            quantidade = solicitacao[2]
            data = solicitacao[3]
            print(f"ID Solicitação: {solicitacao[0]} | Produto ID: {produto_id} | Quantidade: {quantidade} | Data: {data}")
        for produto in produtos: #Melhorando a visualização para saber qual produto esta relacionado.
            produto_id = produto[0]
            produto_nome = produto[1]
            quantidade = produto[3]
            localizacao = produto[5]
            print(f"Produto ID: {produto_id} | Nome do Produto: {produto_nome} | Quantidade: {quantidade} | Localização: {localizacao}")

    conn.close()

def aprovar_rejeitar_solicitacao():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    if(visualizar_solicitacoes_pendentes() == False): #Chamando o método para mostrar novamente as solicitações pendentes, caso a pessoa esqueça.
        return
    #OBS: Caso não existe solicitações, automaticamente ele entra no primeiro if do método visualizar_solicitacoes_pendentes()

    id_solicitacao = int(input("Digite o ID da solicitação: "))
    cursor.execute('SELECT * FROM solicitacoes WHERE id = ? AND status = ?', (id_solicitacao, 'pendente')) # Verifica se a solicitação existe e é pendente.
    solicitacao = cursor.fetchone()

    if solicitacao is None: #Isso aqui é redudante. Pois a função  visualizar_solicitacoes_pendentes(), ja verifica.
        print("Solicitação nao encontrada.")
        conn.close()
        return

    aprovacao = input("Digite 'aprovar' ou 'rejeitar': ")

    if aprovacao.lower() == 'aprovar':
        cursor.execute('SELECT * FROM produtos WHERE id = ?', (solicitacao[1],))
        produto = cursor.fetchone()
        produto_quantidade = produto[3]
        quantidade_comprada = solicitacao[2]
        
        if produto: 
            produto_quantidade = produto[3]
            quantidade_comprada = solicitacao[2]

        if(quantidade_comprada > produto_quantidade):
            print(f"Não temos a quantidade disponivel para aprovação da compra.")
        else:
            nova_quantidade = produto[3] - quantidade_comprada
            cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto[0]))
            print(f"Compra aprovada. Produto {produto[1]} (ID: {produto[0]}) quantidade atualizada.")

            cursor.execute('UPDATE solicitacoes SET status = ? WHERE id = ?', ('aprovada', id_solicitacao))
    
            descricao = f"Solicitação ID: {id_solicitacao}, Produto ID: {produto[0]}, Status de solicitação: {aprovacao}, Comprado: {quantidade_comprada}, Estoque Atual: {nova_quantidade}"
            data_registro = datetime.datetime.now().isoformat()

            cursor.execute('''
                INSERT INTO registros (descricao, data_registro)
                VALUES (?, ?)
            ''', (descricao, data_registro))

    elif aprovacao.lower() == 'rejeitar':
        cursor.execute('UPDATE solicitacoes SET status = ? WHERE id = ?', ('rejeitada', id_solicitacao))

        cursor.execute('SELECT * FROM produtos WHERE id = ?', (solicitacao[1],))
        produto = cursor.fetchone()

        descricao = f"Solicitação ID: {id_solicitacao}, Produto ID: {produto[0]}, Status de solicitação: {aprovacao}, Solicitado: {solicitacao[2]}, Estoque Atual: {produto[3]}"
        data_registro = datetime.datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO registros (descricao, data_registro)
            VALUES (?, ?)
        ''', (descricao, data_registro))

        print("Solicitação rejeitada.")
    else:
        print("Opção de aprovação inválida. Use 'aprovar' ou 'rejeitar'.")

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

def atualizar_localizacao_produto():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, quantidade, localizacao FROM produtos")    
    produtos = cursor.fetchall()

    for produto in produtos:
        id_produto = produto[0]; nome = produto[1]; quantidade = produto[2]; localizacao = produto[3];
        print(f"Produto ID: {id_produto} | Nome do Produto: {nome} | Quantidade: {quantidade}| Localizacao: {localizacao}")

    produto_id = int(input("Digite o ID do produto: "))
    cursor.execute("SELECT id, nome, quantidade, localizacao FROM produtos WHERE id = ?", (produto_id,)) #Busca o produto que ele escolheu.
    produto = cursor.fetchone()

    if produto is None: #Se não encontra o produto cancelar.
        print(f"Produto com ID {produto_id} não encontrado.")
        conn.close()
        return
    
    nome = produto[1]
    quantidade = produto[2]
    localizacao_atual = produto[3]
    print(f"Produto: {nome} | Quantidade: {quantidade} | Localização atual: {localizacao_atual}")
    
    nova_localizacao = input("Digite a nova localização do produto: ")

    cursor.execute('''
        UPDATE produtos
        SET localizacao = ?
        WHERE id = ?
    ''', (nova_localizacao, produto_id))

    conn.commit()

    print(f"Localização do produto '{nome}' (ID: {produto_id}) foi atualizada de '{localizacao_atual}' para '{nova_localizacao}'.")
    alterou_localizacao(nome, produto_id, localizacao_atual, nova_localizacao)

    conn.close()

def alterou_localizacao(nome, produto_id, localizacao_atual, nova_localizacao):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    descricao = f"Produto '{nome}', ID: {produto_id}, Movido de: {localizacao_atual}, Para: {nova_localizacao}"
    data_registro = datetime.datetime.now().isoformat()

    cursor.execute('''
        INSERT INTO registros (descricao, data_registro)
        VALUES (?, ?)
    ''', (descricao, data_registro))

    conn.commit()
    conn.close()

def registros(): #Registro de alterações
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    cursor.execute("SELECT descricao, data_registro FROM registros")    
    registros = cursor.fetchall()

    for registro in registros:
        print(f"Registro: {registro[0]} | Data de registro: {registro[1]}")

    conn.commit()
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
    print("2 - Atualizar Estoque")
    print("3 - Atualizar Localização do Produto")

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
    print("3 - Visualizar todas as Solicitações")
    print("4 - Visualizar registros")

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
                    aprovar_rejeitar_solicitacao()
                elif operacao == '3':
                    visualizar_todas_solicitacoes()
                elif operacao == '4':
                    registros()
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
                elif operacao == '3':
                    atualizar_localizacao_produto()
        elif escolha == '2':
            print("Você selecionou: Usuário")
            while True:
                menu_usuario()
                operacao = input("Digite o número da sua opção: ")
                if operacao == '0': # Voltar para o menu principal
                    break
                elif operacao == '1': # Solicitar compra de produto
                    solicitar_compra()
                elif operacao == '2': # Emitir relatório semanal
                    emitir_relatorio()
                elif operacao == '3': # Mostrar os produtos disponiveis
                    produtos_para_usuario()
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()
