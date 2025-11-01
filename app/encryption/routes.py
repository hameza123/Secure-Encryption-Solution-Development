from flask import Blueprint, request, jsonify, render_template, redirect, url_for, send_file, current_app
from app.encryption.encryption import generate_symmetric_key, encrypt_data, decrypt_data , encrypt_image, decrypt_image
from werkzeug.utils import secure_filename
from app.encryption.key_management import generate_rsa_keypair, save_public_key_to_file, load_private_key, save_private_key_to_file
from app.encryption.key_encryption import encrypt_symmetric_key, decrypt_symmetric_key
from app.encryption.services import generate_encrypted_file, decrypt_file, generate_encrypted_image_file, extract_components_from_file
import os

encryption_bp = Blueprint('encryption', __name__)

@encryption_bp.route('/')
def home():
    return render_template('home.html')



# Route pour afficher le formulaire de chiffrement
@encryption_bp.route('/encrypt', methods=['GET'])
def show_encrypt_form():
    return render_template('encrypt.html')

@encryption_bp.route('/encrypt', methods=['POST'])
def encrypt():
    # Récupérer le texte à chiffrer depuis le formulaire
    plaintext = request.form['plaintext']

    # Récupérer le fichier de clé publique téléchargé
    public_key_file = request.files['public_key_file']
    public_key_pem = public_key_file.read()

    # Générer la clé symétrique AES
    symmetric_key = generate_symmetric_key()

    # Chiffrer la clé symétrique avec la clé publique du destinataire
    try:
        encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, public_key_pem)
    except ValueError as e:
        # Gérer les erreurs de chiffrement si nécessaire
        return f"Erreur lors du chiffrement de la clé symétrique : {e}", 400

    # Chiffrer le texte avec la clé symétrique AES
    iv, ciphertext = encrypt_data(plaintext, symmetric_key)

    # Générer un fichier combiné contenant la clé symétrique chiffrée, l'IV et le texte chiffré
    output_filename = 'encrypted_file.txt'
    generate_encrypted_file(encrypted_symmetric_key, iv, ciphertext, output_filename)

    # Rediriger l'utilisateur vers le téléchargement du fichier chiffré
    return redirect(url_for('encryption.download_file', filename=output_filename))


# Route pour afficher le formulaire de déchiffrement
@encryption_bp.route('/decrypt', methods=['GET'])
def show_decrypt_form():
    return render_template('decrypt.html')

@encryption_bp.route('/decrypt', methods=['POST'])
def decrypt():
    # Obtenez les fichiers téléchargés
    encrypted_file = request.files['encrypted_file']
    private_key_file = request.files['private_key_file']

    # Enregistrez les fichiers dans un répertoire temporaire
    encrypted_file_path = os.path.join('/tmp', encrypted_file.filename)
    encrypted_file.save(encrypted_file_path)
    print(f"Encrypted file saved at: {encrypted_file_path}")

    private_key_path = os.path.join('/tmp', private_key_file.filename)
    private_key_file.save(private_key_path)
    print(f"Private key file saved at: {private_key_path}")

    # Chargez la clé privée depuis le fichier
    private_key = load_private_key(private_key_path)
    print("Private key loaded successfully.")

    # Déchiffrez le fichier
    try:
        plaintext = decrypt_file(encrypted_file_path, private_key_path)
        print("File decrypted successfully.")
    except Exception as e:
        print(f"Error during decryption: {e}")
        return str(e), 400

    # Affichez le texte déchiffré
    print(f"Decrypted plaintext: {plaintext}")
    return render_template('decrypt.html', plaintext=plaintext)

# Route pour permettre de télécharger le fichier chiffré
@encryption_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'Fichier introuvable'}), 404



# Route pour afficher le formulaire de chiffrement des images
@encryption_bp.route('/encrypt-image', methods=['GET'])
def show_encrypt_image_form():
    return render_template('encrypt-image.html')

# Route pour afficher le formulaire de chiffrement
@encryption_bp.route('/encrypt-image', methods=['GET', 'POST'])
def encrypt_image_file():
    # Récupérer l'image téléchargée
    image_file = request.files['image']
    image_path = secure_filename(image_file.filename)
    image_data = image_file.read()

    # Récupérer le fichier de clé publique téléchargé
    public_key_file = request.files['public_key_file']
    public_key_pem = public_key_file.read()

    # Générer la clé symétrique AES
    symmetric_key = generate_symmetric_key()

    # Chiffrer la clé symétrique avec la clé publique du destinataire
    try:
        encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, public_key_pem)
    except ValueError as e:
        # Gérer les erreurs de chiffrement si nécessaire
        return f"Erreur lors du chiffrement de la clé symétrique : {e}", 400

    # Chiffrer le texte avec la clé symétrique AES
    iv, ciphertext = encrypt_image(image_data, symmetric_key)

    # Générer un fichier combiné contenant la clé chiffrée, l'IV, et l'image chiffrée
    output_filename = 'encrypted_image.bin'
    generate_encrypted_image_file(encrypted_symmetric_key, iv, ciphertext, output_filename)

    # Rediriger l'utilisateur vers le téléchargement du fichier chiffré
    return redirect(url_for('encryption.download_file', filename=output_filename))




# Route pour afficher le formulaire de déchiffrement des images 
@encryption_bp.route('/decrypt-image', methods=['GET'])
def show_decrypt_image_form():
    return render_template('decrypt-image.html')


@encryption_bp.route('/decrypt-image', methods=['POST'])
def decrypt_image_file():
    try:
        # Récupérer le fichier combiné téléchargé
        encrypted_file = request.files['encrypted_file']
        private_key_file = request.files['private_key_file']

        # Enregistrer les fichiers dans un répertoire temporaire
        encrypted_file_path = os.path.join('/tmp', encrypted_file.filename)
        encrypted_file.save(encrypted_file_path)
        print(f"Encrypted file saved at: {encrypted_file_path}")

        private_key_path = os.path.join('/tmp', private_key_file.filename)
        private_key_file.save(private_key_path)
        print(f"Private key file saved at: {private_key_path}")

        # Charger la clé privée depuis le fichier
        private_key = load_private_key(private_key_path)
        print("Private key loaded successfully.")

        # Extraire les composants du fichier combiné (clé symétrique chiffrée, IV, et texte chiffré)
        encrypted_symmetric_key, iv, ciphertext = extract_components_from_file(encrypted_file_path)

        # Déchiffrer la clé symétrique avec la clé privée
        try: 
             symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key, private_key)
             print(f"Symmetric key decrypted: {symmetric_key}")
        except Exception as e: 
             print(f"Error decrypting symmetric key: {e}")
             raise

        # Déchiffrer les données de l'image
        image_data = decrypt_image(ciphertext, symmetric_key, iv)

        # Sauvegarder les données déchiffrées dans un fichier image
        output_image_path = os.path.join('/tmp', 'decrypted_image.png')
        save_decrypted_image(image_data, output_image_path)

        # Rediriger vers le téléchargement de l'image déchiffrée
        return send_file(output_image_path, as_attachment=True)

    except Exception as e:
        print(f"Error during decryption: {e}")
        flash("An error occurred during the decryption process.")
        return redirect(url_for('encryption.home'))


def save_decrypted_image(image_data, output_image_path):
    with open(output_image_path, 'wb') as f:
        f.write(image_data)
    
    return output_image_path



# Route pour afficher la page de génération de clés
@encryption_bp.route('/generate_keys_form', methods=['GET'])
def show_generate_keys_form():
    return render_template('generate_keys.html')

@encryption_bp.route('/generate_keys', methods=['GET'])
def generate_keys():
    private_key, public_key = generate_rsa_keypair()

    PRIVATE_KEY_PATH = current_app.config['PRIVATE_KEY_PATH']
    PUBLIC_KEY_PATH = current_app.config['PUBLIC_KEY_PATH']

    save_private_key_to_file(private_key, PRIVATE_KEY_PATH)
    save_public_key_to_file(public_key, PUBLIC_KEY_PATH)

    public_key_filename = 'public_key.pem'
    return redirect(url_for('encryption.download_public_key', filename=public_key_filename))

@encryption_bp.route('/download_public_key/<filename>', methods=['GET'])
def download_public_key(filename):
    public_key_dir = os.path.dirname(current_app.config['PUBLIC_KEY_PATH'])
    public_key_path = os.path.join(public_key_dir, filename)

    if os.path.exists(public_key_path):
        return send_file(public_key_path, as_attachment=True)
    else:
        return jsonify({'error': 'Fichier introuvable'}), 404
