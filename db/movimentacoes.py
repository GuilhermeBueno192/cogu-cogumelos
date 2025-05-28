import logging
from .utils import pesquisar_por_nome

def registrar_movimentacao(conn, cursor, nome_produto, fornecedor, tipo_movimentacao, quantidade, observacao=None):
    try:
        cursor.execute("""
            INSERT INTO movimentacoes_estoque (nome_produto, fornecedor, tipo_movimentacao, quantidade, observacao)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome_produto, fornecedor, tipo_movimentacao, quantidade, observacao))
        conn.commit()
    except Exception as e:
        logging.exception("Erro ao registrar movimentação")
        raise


