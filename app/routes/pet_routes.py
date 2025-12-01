from flask import Blueprint, jsonify, request
from app.model.Pet import Pet
from app.dao.PetDAO import PetDAO

pet_bp = Blueprint('pet_bp', __name__)
dao = PetDAO()

@pet_bp.route('/api/pets', methods=['GET'])
def get_pets():
    lista = dao.listar()
    return jsonify(lista), 200

@pet_bp.route('/api/pets', methods=['POST'])
def criar_pet():
    data = request.json
    # O JSON deve conter: {"nome": "Rex", "dono_id": 1, ...}
    novo_pet = Pet(
        nome=data['nome'],
        dono_id=data['dono_id'],
        especie=data.get('especie'),
        raca=data.get('raca'),
        idade=data.get('idade'),
        peso=data.get('peso')
    )
    pet_salvo = dao.salvar(novo_pet)
    return jsonify(pet_salvo.to_dict()), 201