from flask import Blueprint, jsonify, request
from app.model.Vacina import Vacina
from app.dao.VacinaDAO import VacinaDAO

vacina_bp = Blueprint('vacina_bp', __name__)
dao = VacinaDAO()

@vacina_bp.route('/api/vacinas', methods=['GET'])
def get_vacinas():
    return jsonify(dao.listar()), 200

@vacina_bp.route('/api/vacinas', methods=['POST'])
def criar_vacina():
    data = request.json
    nova_vacina = Vacina(
        data['nome'], 
        data['dataAplicacao'], 
        data['validade'], 
        data['pet_id']
    )
    salva = dao.aplicar(nova_vacina)
    return jsonify(salva.to_dict()), 201
    