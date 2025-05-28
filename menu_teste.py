from db import (
    conectar, pesquisar_por_nome, deletar_por_nome, editar_valor, registrar_movimentacao,
    adicionar_produto, atualizar_quantidade_produto, listar_produtos,
    adicionar_fornecedor, listar_fornecedores, 
)

def iniciar_teste_menu():
    conn, cursor = conectar()

    try:
        while True:
            print("\nMenu:")
            print("1 - Menu produtos")
            print("2 - Menu fornecedores")
            print("3 - entrada/saida produtos")
            print("4 - Visualizar produtos")
            print("5 - Visualizar fornecedores")
            print("6 - Sair")

            opcao1 = input("Escolha uma opção: ")

            if opcao1 == "1":
                print("\nMenu Produtos")
                print("1 - Adicionar Produto")
                print("2 - Editar Produto")
                print("3 - Excluir Produto")
                print("4 - Voltar")

                opcao2 = input("Escolha uma opção: ")

                if opcao2 == "1":
                    nome = input("Nome: ")
                    categoria = input("Categoria: ")
                    descricao = input("Descrição: ")
                    preco = float(input("Preço: "))
                    quantidade = int(input("Quantidade: "))
                    try:
                        adicionar_produto(conn, cursor, nome, categoria, descricao, preco, quantidade)
                        print("Produto adicionado com sucesso.")
                    except Exception as e:
                        print("Erro ao adicionar produto:", e)

                elif opcao2 == "2":
                    nome = input("Nome do produto a editar: ")
                    campo = input("Campo a editar (ex: categoria, preco, descricao, etc): ")
                    novo_valor = input("Novo valor: ")
                    try:
                        editar_valor(conn, cursor, "produtos", campo, novo_valor, "nome", nome)
                        print("Produto editado com sucesso.")
                    except Exception as e:
                        print("Erro ao editar produto:", e)

                elif opcao2 == "3":
                    nome = input("Nome do produto a deletar: ")
                    try:
                        deletar_por_nome(conn, cursor, "produtos", "nome", nome)
                        print("Produto deletado com sucesso.")
                    except Exception as e:
                        print("Erro ao deletar produto:", e)

            if opcao1 == "2":
                print("\nMenu Fornecedores")
                print("1 - Adicionar Fornecedor")
                print("2 - Editar Fornecedor")
                print("3 - Excluir Fornecedor")
                print("4 - Voltar")

                opcao2 = input("Escolha uma opção: ")

                if opcao2 == "1":
                    nome = input("Nome: ")
                    categoria = input("Categoria: ")
                    descricao = input("Descrição: ")
                    try:
                        adicionar_fornecedor(conn, cursor, nome, categoria, descricao)
                        print("Fornecedor adicionado com sucesso.")
                    except Exception as e:
                        print("Erro ao adicionar fornecedor:", e)

                elif opcao2 == "2":
                    nome = input("Nome do fornecedor a editar: ")
                    campo = input("Campo a editar (ex: categoria, descricao, etc): ")
                    novo_valor = input("Novo valor: ")
                    try:
                        editar_valor(conn, cursor, "fornecedor", campo, novo_valor, "nome", nome)
                        print("Fornecedor editado com sucesso.")
                    except Exception as e:
                        print("Erro ao editar fornecedor:", e)

                elif opcao2 == "3":
                    nome = input("Nome do fornecedor a deletar: ")
                    try:
                        deletar_por_nome(conn, cursor, "fornecedor", "nome", nome)
                        print("Fornecedor deletado com sucesso.")
                    except Exception as e:
                        print("Erro ao deletar fornecedor:", e)

            if opcao1 == "3":
                print("\nEntrada/Saída de Produtos")
                print("1 - Entrada de Produtos")
                print("2 - Saída de Produtos")
                print("3 - Voltar ao menu principal")

                opcao2 = input("Escolha uma opção: ")

                if opcao2 in ["1", "2"]:
                    operacao = "entrada" if opcao2 == "1" else "saida"
                    nome_produto = input("Nome do produto: ")
                    fornecedor = input("Fornecedor: ")
                    quantidade = int(input("Quantidade: "))
                    observacao = input("Observação (opcional): ") or None

                    try:
                        atualizar_quantidade_produto(conn, cursor, nome_produto, operacao, quantidade)
                        registrar_movimentacao(conn, cursor, nome_produto, fornecedor, operacao, quantidade, observacao)
                        print(f"{operacao.capitalize()} registrada com sucesso.")
                    except Exception as e:
                        print("Erro ao registrar movimentação:", e)

            if opcao1 == "4":
                print("\nVisualizar Produtos")
                    
                try:
                    produtos = listar_produtos(conn, cursor)
                    for p in produtos:
                        print(p)
                except Exception as e:
                    print("Erro ao listar produtos:", e)

            if opcao1 == "5":
                print("\nVisualizar Fornecedores")
                
                try:
                    fornecedores = listar_fornecedores(conn, cursor)
                    for f in fornecedores:
                        print(f)
                except Exception as e:
                    print("Erro ao listar fornecedores:", e)

            if opcao1 == "6":
                print("\nSaindo...")
                break

    finally:
        conn.close()
        print("Conexão com o banco encerrada.")