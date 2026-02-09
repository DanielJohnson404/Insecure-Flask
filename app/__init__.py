from flask import Flask
from config import Config
from app.utils.db import init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize DB
    init_db()
    
    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.files import files_bp
    from app.routes.admin import admin_bp
    from app.routes.network import network_bp
    from app.routes.api import api_bp
    from app.routes.xml_routes import xml_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(network_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(xml_bp, url_prefix='/xml')
    
    return app
