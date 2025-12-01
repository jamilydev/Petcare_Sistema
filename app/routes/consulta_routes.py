from flask import Blueprint, jsonify, request
from app.model.Consulta import Consulta
from app.dao.ConsultaDAO import ConsultaDAO

consulta_bp = Blueprint('consulta_bp', __name__)
dao = ConsultaDAO()

@consulta_bp.route('/api/consultas', methods=['GET'])
def get_consultas():
    return jsonify(dao.listar()), 200

@consulta_bp.route('/api/consultas', methods=['POST'])
def criar_consulta():
    data = request.json
    nova_consulta = Consulta(
        data['data'], 
        data['hora'], 
        data['veterinario_id'], 
        data['pet_id'], 
        data['motivo']
    )
    salva = dao.agendar(nova_consulta)
    return jsonify(salva.to_dict()), 201
    