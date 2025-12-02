from flask import Blueprint, jsonify, request
from app.model.Veterinario import Veterinario
from app.dao.VeterinarioDAO import VeterinarioDAO

vet_bp = Blueprint('vet_bp', __name__)
dao = VeterinarioDAO()

@vet_bp.route('/api/veterinarios', methods=['GET'])
def get_vets():
    return jsonify(dao.listar()), 200

@vet_bp.route('/api/veterinarios', methods=['POST'])
def criar_vet():
    data = request.json
    # Se senha não for fornecida, usa valor padrão temporário
    senha = data.get('senha', '123456')
    vet = Veterinario(data['nome'], data['crmv'], data['especialidade'], data['telefone'], data['email'], senha)
    salvo = dao.salvar(vet)
    return jsonify(salvo.to_dict()), 201