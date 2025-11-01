# app/config.py
import os

class Config:
    """Configuration de base pour l'application."""

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ENCRYPTED_FILE_DIR = os.path.join(BASE_DIR, 'encrypted_files')
    PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'keys', 'private_key.pem')
    PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'keys', 'public_key.pem')


    SECRET_KEY = os.environ.get('SECRET_KEY', 'vous-devez')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    TESTING = os.environ.get('FLASK_ENV') == 'testing'

    ALLOWED_EXTENSIONS = {'pem', 'txt'}
