from flask import Flask
from datetime import timedelta  # <--- IMPORTANTE: Adicione esta linha

def create_app():
    app = Flask(__name__)
    
    # Chave Secreta
    app.secret_key = 'chave_super_secreta_do_petcare' 

    # --- CONFIGURAÇÃO DE TEMPO DA SESSÃO ---
    # Define que a sessão dura 30 minutos (você pode mudar para days=7 se quiser)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    # ---------------------------------------

    from app.routes.web_routes import web_bp
    app.register_blueprint(web_bp)

    return app