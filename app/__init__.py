from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    # Importa os Blueprints
    from app.routes.dono_routes import dono_bp
    from app.routes.pet_routes import pet_bp
    from app.routes.veterinario_routes import vet_bp
    from app.routes.consulta_routes import consulta_bp
    from app.routes.vacina_routes import vacina_bp  
    from app.routes.recompensa_routes import recompensa_bp
    from app.routes.web_routes import web_bp

    # Registra os Blueprints
    app.register_blueprint(dono_bp)
    app.register_blueprint(pet_bp)
    app.register_blueprint(vet_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(vacina_bp) 
    app.register_blueprint(recompensa_bp) 
    app.register_blueprint(web_bp)

    @app.route('/')
    def home():
        return jsonify({
            "mensagem": "API PetCare Completa!",
            "endpoints": [
                "/api/donos",
                "/api/pets",
                "/api/veterinarios",
                "/api/consultas",
                "/api/vacinas",
                "/api/recompensas"
            ]
        })

    return app