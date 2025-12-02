from flask import Blueprint, jsonify, request
from app.model.Dono import Dono
from app.dao.DonoDAO import DonoDAO

dono_bp = Blueprint('dono_bp', __name__)
dao = DonoDAO()

@dono_bp.route('/api/donos', methods=['GET'])
def get_donos():
    lista = dao.listar()
    return jsonify(lista), 200

@dono_bp.route('/api/donos', methods=['POST'])
def criar_dono():
    try:
        dados = request.json
        # Se senha não for fornecida, usa valor padrão temporário
        senha = dados.get('senha', '123456')
        novo_dono = Dono(dados['nome'], dados['email'], dados['telefone'], senha)
        dono_salvo = dao.salvar(novo_dono)
        return jsonify(dono_salvo.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao criar dono", "detalhes": str(e)}), 500