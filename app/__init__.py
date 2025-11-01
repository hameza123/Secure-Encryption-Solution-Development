# app/__init__.py

from flask import Flask
from app.encryption.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

 

    # Enregistrer les blueprints
    from app.encryption.routes import encryption_bp
    app.register_blueprint(encryption_bp, url_prefix='/')

    return app
