import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
import logging
from db.conexao import conectar
from db.config import DATABASE_CONFIG
from db.produtos import adicionar_produto, atualizar_quantidade_produto, listar_produtos
from db.fornecedor import adicionar_fornecedor, listar_fornecedores
from db.movimentacoes import registrar_movimentacao
from db.utils import pesquisar_por_nome, deletar_por_nome, editar_valor

app = Flask(__name__)
CORS(app)

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Decorador para conexão com o banco de dados
def com_conexao(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn, cursor = conectar()
        if not conn or not cursor:
            logging.error("Erro ao conectar ao banco de dados.")
            return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500
        try:
            return func(conn, cursor, *args, **kwargs)
        except ValueError as ve:
            logging.warning(f"Erro do usuário: {str(ve)}")
            return jsonify({'erro': str(ve)}), 400
        except Exception as e:
            logging.exception(f"Erro interno na função {func.__name__}")
            return jsonify({'erro': 'Erro ao processar a solicitação'}), 500
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception as e:
                logging.error(f"Erro ao fechar a conexão/cursor: {str(e)}")
    return wrapper

# ---------------- TESTE ----------------

@app.route('/teste_conexao', methods=['GET'])
@com_conexao
def teste_conexao(conn, cursor):
    cursor.execute("SELECT 1")
    resultado = cursor.fetchone()
    if resultado:
        return jsonify({'mensagem': 'Conexão com o banco de dados bem-sucedida!'}), 200
    return jsonify({'erro': 'Erro desconhecido ao testar a conexão.'}), 500

# ---------------- ROTAS DE PRODUTOS ----------------

@app.route('/produtos', methods=['GET']) # visualiza produtos
@com_conexao
def get_produtos(conn, cursor):
    produtos = listar_produtos(conn, cursor)
    colunas = [desc[0] for desc in cursor.description]
    produtos_dict = [dict(zip(colunas, row)) for row in produtos]
    return jsonify(produtos_dict)

@app.route('/produto/<nome>', methods=['GET']) # visualiza produto
@com_conexao
def visualizar_produto(conn, cursor, nome):
    try:
        produto = pesquisar_por_nome(cursor, 'produtos', 'nome', nome)
        return jsonify(produto), 200
    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 404
    except Exception:
        logging.exception("Erro ao buscar produto")
        return jsonify({'erro': 'Erro interno ao buscar produto.'}), 500

@app.route('/produtos', methods=['POST']) # adiciona produtos
@com_conexao
def post_produto(conn, cursor):
    dados = request.get_json()
    campos = ['nome', 'categoria', 'descricao', 'preco', 'quantidade']
    for campo in campos:
        if campo not in dados:
            return jsonify({'erro': f'Campo obrigatório "{campo}" ausente.'}), 400

    try:
        adicionar_produto(
            conn, cursor,
            dados['nome'], dados['categoria'],
            dados['descricao'], dados['preco'], dados['quantidade'])
        return jsonify({'mensagem': 'Produto adicionado com sucesso!'}), 201
    except Exception as e:
        logging.exception("Erro ao adicionar produto")
        return jsonify({'erro': 'Erro ao adicionar produto.'}), 500

@app.route('/deletar_produto/<nome>', methods=['DELETE']) # deleta produtos
@com_conexao
def deletar_produto_nome(conn, cursor, nome):
    try:
        deletar_por_nome(conn, cursor, 'produtos', 'nome', nome)
        return jsonify({'mensagem': f'Produto "{nome}" deletado com sucesso.'}), 200
    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 404
    except Exception:
        logging.exception("Erro ao deletar produto")
        return jsonify({'erro': 'Erro interno ao deletar produto.'}), 500

@app.route('/produtos/estoque', methods=['PUT']) # atualiza quantidade de estoque e registra
@com_conexao
def atualizar_estoque(conn, cursor):
    dados = request.get_json()
    campos = ['operacao', 'fornecedor', 'nome_produto', 'quantidade']
    for campo in campos:
        if campo not in dados:
            return jsonify({'erro': f'Campo "{campo}" ausente.'}), 400

    try:
        # Atualiza a tabela de produtos
        atualizar_quantidade_produto(
            conn, cursor,
            dados['nome_produto'],
            dados['operacao'],
            dados['quantidade']
        )

        # Registra a movimentação no histórico
        registrar_movimentacao(
            cursor,
            nome_produto=dados['nome_produto'],
            fornecedor=dados['fornecedor'],
            tipo_movimentacao=dados['operacao'],
            quantidade=dados['quantidade'],
            observacao=dados.get('observacao')  # Pode ser None se não vier no JSON
        )

        return jsonify({'mensagem': 'Estoque atualizado e movimentação registrada com sucesso!'}), 200

    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 400
    except Exception:
        logging.exception("Erro ao atualizar estoque")
        return jsonify({'erro': 'Erro ao atualizar estoque.'}), 500

@app.route("/produtos/editar", methods=["PUT"]) # atualiza informação do produto
@com_conexao
def editar_produto(conn, cursor):
    data = request.get_json()

    nome_produto = data.get("nome_produto")  # nome atual que será usado como filtro
    campo = data.get("campo")  # nome da coluna a ser alterada
    novo_valor = data.get("novo_valor")

    if not all([nome_produto, campo, novo_valor]):
        return jsonify({"erro": "Campos obrigatórios: nome_produto, campo, novo_valor"}), 400

    try:
        editar_valor(conn, cursor, "produtos", campo, novo_valor, "nome", nome_produto)
        return jsonify({"mensagem": f"{campo} do produto '{nome_produto}' atualizado com sucesso."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ---------------- ROTAS DE FORNECEDORES ----------------

@app.route('/fornecedor', methods=['GET']) # visualiza fornecedores
@com_conexao
def get_fornecedores(conn, cursor):
    fornecedores = listar_fornecedores(conn, cursor)
    colunas = [desc[0] for desc in cursor.description]
    fornecedores_dict = [dict(zip(colunas, row)) for row in fornecedores]
    return jsonify(fornecedores_dict)

@app.route('/fornecedor/<nome>', methods=['GET']) # visualiza fornecedore especifico
@com_conexao
def visualizar_fornecedor(conn, cursor, nome):
    try:
        fornecedor = pesquisar_por_nome(cursor, 'fornecedor', 'nome', nome)
        return jsonify(fornecedor), 200
    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 404
    except Exception:
        logging.exception("Erro ao buscar fornecedor")
        return jsonify({'erro': 'Erro interno ao buscar fornecedor.'}), 500

@app.route('/fornecedor', methods=['POST']) # adiciona novo fornecedor
@com_conexao
def post_fornecedor(conn, cursor):
    dados = request.get_json()
    campos = ['nome', 'categoria', 'descricao']
    for campo in campos:
        if campo not in dados:
            return jsonify({'erro': f'Campo obrigatório "{campo}" ausente.'}), 400

    try:
        adicionar_fornecedor(
            conn, cursor,
            dados['nome'], dados['categoria'],
            dados['descricao']
        )
        return jsonify({'mensagem': 'Fornecedor adicionado com sucesso!'}), 201
    except Exception as e:
        logging.exception("Erro ao adicionar fornecedor")
        return jsonify({'erro': 'Erro ao adicionar fornecedor.'}), 500

@app.route('/deletar_fornecedor/<nome>', methods=['DELETE']) # deleta fornecedor
@com_conexao
def deletar_fornecedor_nome(conn, cursor, nome):
    try:
        deletar_por_nome(conn, cursor, 'fornecedor', 'nome', nome)
        return jsonify({'mensagem': f'Fornecedor "{nome}" deletado com sucesso.'}), 200
    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 404
    except Exception:
        logging.exception("Erro ao deletar fornecedor")
        return jsonify({'erro': 'Erro interno ao deletar fornecedor.'}), 500

@app.route("/fornecedores/editar", methods=["PUT"]) # atualiza informação do fornecedor
@com_conexao
def editar_fornecedor(conn, cursor):
    data = request.get_json()

    nome_fornecedor = data.get("nome_fornecedor")  # usado como filtro
    campo = data.get("campo")  # coluna a ser alterada
    novo_valor = data.get("novo_valor")

    if not all([nome_fornecedor, campo, novo_valor]):
        return jsonify({"erro": "Campos obrigatórios: nome_fornecedor, campo, novo_valor"}), 400

    try:
        editar_valor(conn, cursor, "fornecedor", campo, novo_valor, "nome", nome_fornecedor)
        return jsonify({"mensagem": f"{campo} do fornecedor '{nome_fornecedor}' atualizado com sucesso."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
# ---------------- EXECUÇÃO ----------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)