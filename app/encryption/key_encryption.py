from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

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
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as f:
        f.write(pem)

def save_public_key_to_file(public_key, filename):
    """Sauvegarde la clé publique dans un fichier."""
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as f:
        f.write(pem)

def load_private_key(filename):
    """Charge la clé privée depuis un fichier."""
    with open(filename, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
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


from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def encrypt_symmetric_key(symmetric_key, public_key):
    """Chiffre la clé symétrique avec la clé publique RSA."""
    # Vérifiez si public_key est déjà un objet RSAPublicKey
    if isinstance(public_key, bytes):
        public_key = serialization.load_pem_public_key(public_key, backend=default_backend())

    # Chiffrement de la clé symétrique avec la clé publique
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_symmetric_key

def decrypt_symmetric_key(encrypted_symmetric_key, private_key):
    """Déchiffre la clé symétrique à l'aide de la clé privée RSA."""
    # Vérifier la taille du texte chiffré et de la clé privée
    key_size = private_key.key_size // 8  # Convertir en octets
    if len(encrypted_symmetric_key) != key_size:
        raise ValueError(f"Longueur du texte chiffré ({len(encrypted_symmetric_key)}) ne correspond pas à la taille de la clé privée ({key_size}).")

    # Déchiffrer la clé symétrique
    symmetric_key = private_key.decrypt(
        encrypted_symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return symmetric_key


