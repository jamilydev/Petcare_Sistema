from flask import Blueprint, jsonify, request
from app.model.Recompensa import Recompensa
from app.dao.RecompensaDAO import RecompensaDAO

recompensa_bp = Blueprint('recompensa_bp', __name__)
dao = RecompensaDAO()

# Consultar pontos de um dono específico
@recompensa_bp.route('/api/recompensas/<int:dono_id>', methods=['GET'])
def get_pontos(dono_id):
    recompensa = dao.buscar_por_dono(dono_id)
    if recompensa:
        return jsonify(recompensa), 200
    return jsonify({"mensagem": "Dono sem pontuação registrada"}), 404

# Adicionar/Atualizar pontos
@recompensa_bp.route('/api/recompensas', methods=['POST'])
def atualizar_pontos():
    data = request.json
    nova_recompensa = Recompensa(
        pontos=data['pontos'],
        nivel=data['nivel'],
        dono_id=data['dono_id']
    )
    dao.salvar_ou_atualizar(nova_recompensa)
    return jsonify({"mensagem": "Pontuação atualizada com sucesso!"}), 200
    