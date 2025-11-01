# test_encryption.py

from app.encryption.encryption import generate_symmetric_key, encrypt_data, decrypt_data

def test_encrypt_decrypt_data():
    # Données à chiffrer
    plaintext = "Ceci est un test de chiffrement."

    # Génération de la clé symétrique
    key = generate_symmetric_key()

    # Chiffrement des données
    iv, ciphertext = encrypt_data(plaintext, key)

    # Déchiffrement des données
    decrypted_text = decrypt_data(iv, ciphertext, key)

    # Vérifiez si le texte déchiffré correspond à l'original
    assert decrypted_text == plaintext
