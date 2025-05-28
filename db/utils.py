import logging

def pesquisar_por_nome(cursor, tabela, nome_coluna, nome_valor):
    try:
        cursor.execute(f"SELECT * FROM {tabela} WHERE {nome_coluna} = %s", (nome_valor,))
        resultado = cursor.fetchone()
        if not resultado:
            raise ValueError(f"{tabela.capitalize()} com nome '{nome_valor}' não encontrado.")
        colunas = [desc[0] for desc in cursor.description]
        return dict(zip(colunas, resultado))
    except Exception as e:
        logging.exception(f"Erro ao pesquisar em {tabela}")
        raise e

def editar_valor(conn, cursor, tabela, coluna_para_alterar, novo_valor, coluna_filtro, valor_filtro):
    try:
        # Verifica se o item existe antes de tentar atualizar
        _ = pesquisar_por_nome(cursor, tabela, coluna_filtro, valor_filtro)

        sql = f"UPDATE {tabela} SET {coluna_para_alterar} = %s WHERE {coluna_filtro} = %s"
        cursor.execute(sql, (novo_valor, valor_filtro))
        conn.commit()

        logging.info(f"Atualização feita: {coluna_para_alterar} alterada para '{novo_valor}' em {tabela} onde {coluna_filtro} = '{valor_filtro}'.")
    except Exception as e:
        logging.error(f"Erro ao atualizar {coluna_para_alterar} em {tabela}: {e}")
        raise

def deletar_por_nome(conn, cursor, tabela, nome_coluna, nome_valor):
    try:
        _ = pesquisar_por_nome(cursor, tabela, nome_coluna, nome_valor)
        cursor.execute(f"DELETE FROM {tabela} WHERE {nome_coluna} = %s", (nome_valor,))
        conn.commit()
        logging.info(f"{tabela.capitalize()} '{nome_valor}' excluído com sucesso.")
    except Exception as e:
        logging.exception(f"Erro ao deletar de {tabela}")
        raise
