import logging
from .utils import pesquisar_por_nome

def registrar_movimentacao(cursor, nome_produto, fornecedor, tipo, quantidade, observacao=None):
    try:
        cursor.execute("""
            INSERT INTO movimentacoes (nome_produto, fornecedor, tipo, quantidade, observacao)
            VALUES (?, ?, ?, ?, ?)
        """, (nome_produto, fornecedor, tipo, quantidade, observacao))
    except Exception as e:
        logging.exception("Erro ao registrar movimentação")
        raise


