import logging
from .utils import pesquisar_por_nome

def adicionar_fornecedor(conn, cursor, nome, categoria, descricao, quantidade):
    try:
        if not nome or quantidade < 0:
            raise ValueError("Dados inválidos para cadastro de fornecedor.")
        sql = "INSERT INTO fornecedor (nome, categoria, descricao, quantidade) VALUES (%s, %s, %s, %s)"
        valores = (nome, categoria, descricao, quantidade)
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