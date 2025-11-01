import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from app.encryption.key_encryption import  decrypt_symmetric_key
from app.encryption.key_management import generate_rsa_keypair, save_public_key_to_file, load_private_key, load_public_key


def generate_symmetric_key():
    return os.urandom(32)  # 256 bits pour AES

def encrypt_data(plaintext, symmetric_key):
    iv = os.urandom(16)  # IV de 16 octets
    print(f"Generated IV: {iv}")

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Padding des données
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    print(f"Padded data: {padded_data}")

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    print(f"Ciphertext: {ciphertext}")

    return iv, ciphertext

def decrypt_data(ciphertext, symmetric_key, iv):
    print(f"IV for decryption: {iv}")
    print(f"Ciphertext for decryption: {ciphertext}")

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    print(f"Padded data after decryption: {padded_data}")

    # Retrait du padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    print(f"Plaintext after unpadding: {plaintext.decode()}")

    return plaintext.decode()


def encrypt_image(image_data, symmetric_key):
    iv = os.urandom(16)  # IV de 16 octets (128 bits)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Appliquer un padding pour ajuster à la taille du bloc AES
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(image_data) + padder.finalize()

    # Chiffrer les données
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext


 




def decrypt_image(ciphertext, symmetric_key, iv):
    # Créer l'objet Cipher avec la clé symétrique et l'IV
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    # Déchiffrer les données
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Retirer le padding PKCS7 pour obtenir les données originales
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    image_data = unpadder.update(padded_data) + unpadder.finalize()

    return image_data




