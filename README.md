# My Encryption App

## Description

My Encryption App est une application web sécurisée pour le chiffrement et le déchiffrement de fichiers. Elle utilise des algorithmes de chiffrement symétrique et asymétrique pour protéger les données sensibles. Les utilisateurs peuvent générer des paires de clés RSA, chiffrer des textes et des fichiers avec une clé symétrique, et déchiffrer des fichiers en utilisant des clés privées.

## Fonctionnalités

- **Génération de Clés RSA** : Crée des paires de clés RSA publiques et privées.
- **Chiffrement de Données** : Chiffre les textes en utilisant une clé symétrique AES et la clé publique RSA du destinataire.
- **Déchiffrement de Données** : Déchiffre les fichiers en utilisant la clé privée RSA.
- **Téléchargement des Clés** : Permet le téléchargement de la clé publique générée pour le chiffrement.

## Prérequis

- Python 3.6 ou version ultérieure
- Flask
- PyCryptodome

## Installation

1. **Clonez le dépôt :**
```bash
git clone https://github.com/hameza123/Secure-Encryption-Solution-Development.git
cd Secure-Encryption-Solution-Development
```

2. **Créez et activez un environnement virtuel :**
```bash
python3 -m venv venv
```
**Pour Windows :**
```bash
venv\Scripts\activate
```
**Pour macOS et Linux :**
```bash
source venv/bin/activate
```

3. **Installez les dépendances :**
```bash
pip install -r requirements.txt
```

4. **Démarrez l'application :**
```bash
flask run
```
L'application sera accessible à l'adresse `http://127.0.0.1:5000/`

## Utilisation

1. **Accédez à la page d'accueil** : `http://127.0.0.1:5000/`

2. **Générez des clés RSA :**
   - Allez sur la page "Generate Keys"
   - Cliquez sur le bouton pour générer des clés

3. **Chiffrez des données :**
   - Allez sur la page "Encrypt"
   - Téléversez le fichier de clé publique
   - Entrez le texte à chiffrer
   - Cliquez sur "Encrypt"

4. **Déchiffrez des données :**
   - Allez sur la page "Decrypt"
   - Téléversez le fichier chiffré et le fichier de clé privée
   - Cliquez sur "Decrypt"

## Contribution

Les contributions sont les bienvenues ! Veuillez soumettre une demande de tirage (pull request) ou ouvrir une issue pour discuter des modifications souhaitées.

## License

Ce projet est sous la licence MIT. Voir le fichier LICENSE pour plus de détails.

## Contact

Pour toute question, veuillez me contacter à [Linkedin](https://www.linkedin.com/in/hamzarahmani1)

---

Merci d'utiliser My Encryption App ! Nous espérons qu'elle vous sera utile pour vos besoins de chiffrement et déchiffrement de données.
