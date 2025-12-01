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
    dados = request.json
    novo_dono = Dono(dados['nome'], dados['email'], dados['telefone'])
    dono_salvo = dao.salvar(novo_dono)
    return jsonify(dono_salvo.to_dict()), 201