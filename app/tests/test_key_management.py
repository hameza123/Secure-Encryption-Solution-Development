# test_key_management.py

from app.encryption.key_management import generate_rsa_keypair

def test_generate_rsa_keypair():
    # Générer une paire de clés RSA
    private_key, public_key = generate_rsa_keypair()

    # Vérifiez si les clés ne sont pas None
    assert private_key is not None
    assert public_key is not None

    # Test de format PEM
    assert private_key.startswith(b'-----BEGIN PRIVATE KEY-----')
    assert public_key.startswith(b'-----BEGIN PUBLIC KEY-----')
