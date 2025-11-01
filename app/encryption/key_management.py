from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os

def generate_rsa_keypair():
    """Génère une paire de clés RSA."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_private_key_to_file(private_key, filename):
    """Sauvegarde la clé privée dans un fichier."""
    # Crée le dossier si nécessaire
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as f:
        f.write(pem)

def save_public_key_to_file(public_key, filename):
    """Sauvegarde la clé publique dans un fichier."""
    # Crée le dossier si nécessaire
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as f:
        f.write(pem)

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def load_private_key(private_key_path):
    # Lire la clé privée à partir du fichier
    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # Si la clé privée est protégée par un mot de passe, spécifiez-le ici
            backend=default_backend()
        )
    return private_key



def load_public_key(filename):
    """Charge la clé publique depuis un fichier."""
    with open(filename, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key
