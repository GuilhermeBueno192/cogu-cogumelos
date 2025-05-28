import logging
from .utils import pesquisar_por_nome

def adicionar_fornecedor(conn, cursor, nome, categoria, descricao):
    try:
        if not nome:
            raise ValueError("Nome é obrigatório.")
        sql = "INSERT INTO fornecedor (nome, categoria, descricao) VALUES (%s, %s, %s)"
        valores = (nome, categoria, descricao)
        cursor.execute(sql, valores)
        conn.commit()
        logging.info(f"Fornecedor '{nome}' adicionado com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao adicionar fornecedor '{nome}': {e}")
        raise

def listar_fornecedores(conn, cursor):
    try:
        cursor.execute("SELECT * FROM fornecedor")
        return cursor.fetchall()
    except Exception as e:
        logging.error(f"Erro ao listar fornecedores: {e}")
        raise