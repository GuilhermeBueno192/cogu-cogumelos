import logging
from .utils import pesquisar_por_nome

def adicionar_produto(conn, cursor,nome,categoria,descricao,preco,quantidade):
    try:
        if not nome or preco < 0 or quantidade < 0:
            raise ValueError("Dados inválidos para cadastro de produto.")
        sql = "INSERT INTO produtos (nome, categoria, descricao, preco, quantidade) VALUES (%s, %s, %s, %s, %s)"
        valores = (nome, categoria, descricao, preco, quantidade)
        cursor.execute(sql, valores)
        conn.commit()
        logging.info(f"Produto '{nome}' adicionado com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao adicionar produto '{nome}': {e}")
        raise

def listar_produtos(conn, cursor):
    try:
        cursor.execute("SELECT * FROM produtos")
        return cursor.fetchall()
    except Exception as e:
        logging.error(f"Erro ao listar produtos: {e}")
        raise

def atualizar_quantidade_produto(conn, cursor, nome_produto, operacao, quantidade_alteracao):
    try:
        sql_busca = "SELECT codigo, quantidade FROM produtos WHERE nome = %s"
        cursor.execute(sql_busca, (nome_produto,))
        resultado = cursor.fetchone()

        if resultado is None:
            raise ValueError(f"Produto '{nome_produto}' não encontrado.")

        produto_codigo, quantidade_atual = resultado

        if operacao.lower() == "entrada":
            nova_quantidade = quantidade_atual + quantidade_alteracao
        elif operacao.lower() == "saida":
            if quantidade_alteracao > quantidade_atual:
                raise ValueError(
                    f"Não há estoque suficiente para remover {quantidade_alteracao} unidades de '{nome_produto}'. Estoque atual: {quantidade_atual}."
                )
            nova_quantidade = quantidade_atual - quantidade_alteracao
        else:
            raise ValueError("Operação inválida! Use 'entrada' ou 'saida'.")

        sql_update = "UPDATE produtos SET quantidade = %s WHERE codigo = %s"
        cursor.execute(sql_update, (nova_quantidade, produto_codigo))
        conn.commit()
        logging.info(f"Quantidade do produto '{nome_produto}' atualizada com sucesso. Nova quantidade: {nova_quantidade}.")
    except Exception as e:
        logging.error(f"Erro ao atualizar quantidade do produto '{nome_produto}': {e}")
        raise