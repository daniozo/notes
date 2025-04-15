# NoteKeeper - Application Django de gestion de notes

## Description
Une application de gestion de notes simple mais complète, développée avec Django et PostgreSQL.

## Fonctionnalités
- Création, édition et suppression de notes
- Authentification et gestion des utilisateurs
- Interface utilisateur avec TailwindCSS et Lucide Icons

## Technologies utilisées
- Django
- PostgreSQL
- TailwindCSS
- Docker & Docker Compose
- pytest pour les tests
- GitHub Actions pour CI/CD

## Installation et démarrage

### Méthode 1: Sans Docker (développement local)
```bash
# Cloner le repo
git clone <repo-url>
cd notes

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
# Assurez-vous que PostgreSQL est installé et en cours d'exécution
# Puis créez un fichier .env avec les variables nécessaires

# Appliquer les migrations
python manage.py migrate

# Créer un super utilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

### Méthode 2: Avec Docker (recommandé)
```bash
# Cloner le repo
git clone <repo-url>
cd notes

# Démarrer avec Docker Compose
docker-compose up -d

# Créer un super utilisateur
docker-compose exec web python manage.py createsuperuser
```

## Tests
Pour exécuter les tests:

```bash
# Sans Docker
pytest

# Avec Docker
docker-compose exec web pytest
```

## Structure du projet
notes/
├── app/                    # Application principale
├── notes/                  # Configuration du projet
├── templates/              # Templates HTML
├── tests/                  # Tests unitaires
├── static/                 # Fichiers statiques
├── manage.py               # Script de gestion Django
├── Dockerfile              # Configuration Docker
├── docker-compose.yml      # Configuration Docker Compose
├── requirements.txt        # Dépendances Python
├── pytest.ini              # Configuration pytest
└── .env                    # Variables d'environnement