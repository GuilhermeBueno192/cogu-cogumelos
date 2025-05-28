from db.conexao import conectar
from db.config import DATABASE_CONFIG
from db.produtos import adicionar_produto, atualizar_quantidade_produto, listar_produtos
from db.fornecedor import adicionar_fornecedor, listar_fornecedores
from db.movimentacoes import registrar_movimentacao
from db.utils import pesquisar_por_nome, deletar_por_nome, editar_valor