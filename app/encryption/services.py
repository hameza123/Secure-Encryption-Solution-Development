from app.encryption.key_management import generate_rsa_keypair, save_public_key_to_file, load_private_key, load_public_key
from app.encryption.encryption import generate_symmetric_key, encrypt_data
from app.encryption.key_encryption import encrypt_symmetric_key, decrypt_symmetric_key

def generate_encrypted_file(encrypted_symmetric_key, iv, ciphertext, output_filename):
    with open(output_filename, 'wb') as file:
        # Écrire la clé symétrique chiffrée
        file.write(encrypted_symmetric_key)
        # Écrire le vecteur d'initialisation (IV)
        file.write(iv)
        # Écrire le texte chiffré
        file.write(ciphertext)


from app.encryption.key_management import load_private_key
from app.encryption.key_encryption import decrypt_symmetric_key
from app.encryption.encryption import decrypt_data

def decrypt_file(encrypted_file_path, private_key_path):
    print(f"Loading private key from: {private_key_path}")
    private_key = load_private_key(private_key_path)

    with open(encrypted_file_path, 'rb') as f:
        encrypted_symmetric_key = f.read(256)  # Assuming RSA key size is 2048 bits (256 bytes)
        print(f"Encrypted symmetric key read: {encrypted_symmetric_key}")

        iv = f.read(16)  # Read IV (16 bytes for AES)
        print(f"IV read: {iv}")

        ciphertext = f.read()  # Read the rest as ciphertext
        print(f"Ciphertext read: {ciphertext}")

    try:
        symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key, private_key)
        print(f"Symmetric key decrypted: {symmetric_key}")
    except Exception as e:
        print(f"Error decrypting symmetric key: {e}")
        raise

    try:
        plaintext = decrypt_data(ciphertext, symmetric_key, iv)
        print(f"Decrypted plaintext: {plaintext}")
    except Exception as e:
        print(f"Error decrypting data: {e}")
        raise

    return plaintext


# Fonction pour générer un fichier combiné (clé chiffrée, IV, données chiffrées)
def generate_encrypted_image_file(encrypted_key, iv, ciphertext, output_filename):
    with open(output_filename, 'wb') as output_file:
        output_file.write(encrypted_key + iv + ciphertext)


def extract_components_from_file(encrypted_file_path):
    with open(encrypted_file_path, 'rb') as f:
        # Lire la clé symétrique chiffrée (supposons 256 octets pour RSA)
        encrypted_symmetric_key = f.read(256)
        print(f"Encrypted symmetric key read: {encrypted_symmetric_key}")

        # Lire l'IV (16 octets pour AES)
        iv = f.read(16)
        print(f"IV read: {iv}")

        # Lire le reste comme les données chiffrées
        ciphertext = f.read()
        print(f"Ciphertext read: {ciphertext}")

    return encrypted_symmetric_key, iv, ciphertext


