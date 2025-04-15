# 🧪 TP DevOps Django : Dockerisation + Tests + CI

## Objectif du TP

À la fin de ce TP, vous serez capables de :
* Configurer un projet Django proprement pour l'environnement local et Docker.
* Dockeriser l'application avec PostgreSQL.
* Écrire et exécuter des tests unitaires avec pytest.
* Configurer un pipeline CI GitHub qui valide chaque push.

## 1️⃣ Préparer le projet Django

### Étape 1 : Vérifier la structure du projet

Si votre projet n'est pas déjà structuré comme ci-dessous, réorganisez-le :

```
mon_projet/
├── backend/                  # Dossier principal Django
│   ├── manage.py
│   ├── mon_projet/           # Dossier de settings
│   └── app/                  # Votre app Django
├── backend/tests/            # Dossier pour les tests
├── requirements.txt
├── pytest.ini
├── Dockerfile
├── docker-compose.yml
├── .env
├── .dockerignore
└── .github/workflows/ci.yml
```

**Important** : le dossier `venv/` ne doit jamais être dans votre repo !

## 2️⃣ Configurer Django proprement

### Étape 2 : Modifier le fichier settings.py

Remplacez les valeurs fixes par des variables d'environnement pour faciliter la configuration dans Docker.

```python
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-secret')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432')
    }
}
```

### Étape 3 : Créer le fichier .env

Dans la racine du projet, crée un fichier `.env` :

```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DEBUG=True
SECRET_KEY=mysecretkey
```

Pourquoi `HOST=db` plus tard ? Parce que dans Docker Compose, le conteneur PostgreSQL s'appelle `db`.

### Étape 5 : Créer un fichier .gitignore

Dans la racine du projet :

```bash
touch .gitignore
```

Ajoutez :

```
__pycache__/
*.pyc
.env
venv/
postgres_data/
```

## 3️⃣ Ajouter les tests unitaires

Avant de dockeriser, on teste toujours le projet en local. C'est une règle d'or : ne jamais dockeriser du code potentiellement cassé.

### Étape 6 : Installer Pytest et configurer le projet

**Pourquoi Pytest ?**
* Plus simple que unittest de Python natif.
* Compatible avec Django via pytest-django.
* Permet de marquer les tests avec des décorateurs (@pytest.mark...).

**Installer les bibliothèques nécessaires**

Dans votre environnement virtuel local (dans le dossier du projet) :

```bash
pip install pytest pytest-django
```

Ajoutez ensuite ces bibliothèques dans votre requirements.txt :

```bash
pip freeze > requirements.txt
```

### Étape 7 : Créer un fichier pytest.ini

Ce fichier dit à Pytest où trouver les paramètres Django, et quels fichiers de test il doit scanner.

Dans la racine du projet, créez un fichier nommé `pytest.ini` :

```ini
[pytest]
DJANGO_SETTINGS_MODULE = mon_projet.settings
python_files = tests.py test_*.py *_test.py
```

* `DJANGO_SETTINGS_MODULE` : pointeur vers vos settings.py.
* `python_files` : indique les formats de noms de fichiers que pytest doit exécuter automatiquement.

### Étape 8 : Écrire un premier test de base de données

Créez un fichier `backend/tests/test_model.py`, et ajoutez :

```python
import pytest
from app.models import MonModele

@pytest.mark.django_db
def test_model_creation():
    obj = MonModele.objects.create(nom="Test")
    assert obj.id is not None
```

**Explication :**
* `@pytest.mark.django_db` : autorise l'accès à la base de données dans ce test.
* `MonModele.objects.create(...)` : crée un objet dans la table.
* `assert obj.id is not None` : vérifie que l'objet a bien été inséré (et qu'un id a été généré).

Ce test valide que :
* la connexion à PostgreSQL fonctionne ;
* la table existe dans la base ;
* Django peut écrire dedans sans erreur.

### Étape 9 : Lancer les tests localement

Dans le terminal (toujours dans le dossier projet) :

```bash
pytest
```

Vous devriez voir apparaître un message comme :

```
collected 1 item
test_model.py . [100%]
```

### Étape 10 : Générer requirements.txt

Dans votre environnement virtuel local :

```bash
pip freeze > requirements.txt
```

## 4️⃣ Dockerisation de Django + PostgreSQL

### Étape 11 : Créer le fichier .dockerignore

```bash
touch .dockerignore
```

Ajoutez :

```
venv/
__pycache__/
*.pyc
.env
postgres_data/
```

### Étape 12 : Créer un Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
```

### Étape 13 : Créer docker-compose.yml

```yaml
version: '3.9'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - .:/app
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

### Étape 14 : Lancer votre projet et tester

```bash
docker-compose up --build -d
docker-compose exec web python backend/manage.py migrate
docker-compose exec web pytest
```

## 5️⃣ Intégration Continue GitHub (CI)

### Étape 15 : Créer le dossier .github/workflows

```bash
mkdir -p .github/workflows
touch .github/workflows/ci.yml
```

### Étape 16 : Ajouter le fichier ci.yml

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: postgres
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    env:
      DB_NAME: postgres
      DB_USER: postgres
      DB_PASSWORD: postgres
      DB_HOST: localhost
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

## 6️⃣ Protéger la branche main et travailler proprement

Avant d'autoriser vos collaborateurs à contribuer sur le projet, vous devez protéger la branche principale `main` pour :

* Éviter que quelqu'un pousse du code cassé directement
* Forcer le passage par Pull Request + tests automatisés
* Appliquer un workflow d'équipe professionnel

### Étape 1 : Créer le dépôt GitHub

1. Va sur https://github.com/new
2. Remplis :
   - Repository name : tp-django-devops (par exemple)
   - Coche Private si c'est pour un TP
   - Ne coche pas "Add README" (on le fera à la main)
3. Clique sur Create repository

### Étape 2 : Initialiser ton dépôt Git local

Dans ton dossier projet en local (sur ton PC) :

```bash
git init
git add .
git commit -m "Initial commit : Django app with Docker and Pytest"
```

Ajoute le dépôt distant :

```bash
git remote add origin https://github.com/<ton-nom-utilisateur>/tp-django-devops.git
git push -u origin main
```

### Étape 3 : Protéger la branche main

Sur GitHub :
1. Va dans Settings > Branches
2. Clique sur Add branch rule
3. Dans "Branch name pattern" : écris main
4. Active les options suivantes :
   - Require status checks to pass before merging
   - Require a pull request before merging
   - (optionnel) Include administrators

Cela bloque les push directs sur main : tout changement doit passer par une PR (pull request) + tests validés.

## 7️⃣ Cycle de contribution complet (Workflow Git + PR)

Maintenant que main est protégé, voici comment contribuer proprement :

### Étape 4 : Créer une nouvelle branche pour travailler

Dans le terminal :

```bash
git checkout -b feature/ajout-test-modele
```

Le nom de la branche décrit la tâche (nouveau test, bugfix, feature...).

### Étape 5 : Coder et tester

Ajoute ton code dans models.py, écris un test, lance pytest, assure-toi que tout est OK.

### Étape 6 : Commiter les changements

```bash
git add .
git commit -m "feat: ajout d'un test pour la création d'un modèle"
```

### Étape 7 : Pousser sur GitHub

```bash
git push origin feature/ajout-test-modele
```

### Étape 8 : Ouvrir une Pull Request

1. Sur GitHub, va sur ton repo.
2. Clique sur le bouton Compare & pull request.
3. Rédige un titre clair + une description.
4. Clique sur Create Pull Request.

### Étape 9 : GitHub Actions vérifie les tests

Automatiquement :
* GitHub exécute le fichier `.github/workflows/ci.yml`
* Si tous les tests sont OK, le merge est possible

### Étape 10 : Merge la PR (ou attends l'approbation)

* Soit tu merges toi-même si tu es seul
* Soit tu attends une validation par un collègue ou ton formateur

## ✅ Annexes et améliorations pédagogiques

### 🔧 Pré-requis

Ce TP suppose que les logiciels suivants sont installés sur votre machine :
- Python (3.10 ou plus)
- pip
- Git
- Docker Desktop

Si ce n'est pas le cas, suivez les guides d'installation correspondants ou demandez à votre formateur.

### 📦 Pourquoi utiliser des variables d'environnement ?

Les variables d'environnement permettent de rendre la configuration du projet dynamique. Au lieu d'écrire des valeurs fixes (comme un mot de passe ou un nom de base de données) dans le code, on les externalise dans un fichier `.env`. Cela améliore la sécurité et la flexibilité.

### 🐳 Pourquoi HOST = 'db' ?

Dans un fichier `docker-compose.yml`, chaque service possède un nom de réseau. Par exemple, si vous avez :

```yaml
services:
  db:
    image: postgres:15
```

Alors le service Django (`web`) devra utiliser `DB_HOST=db` car `db` devient un nom DNS interne dans le réseau Docker.

### 🧪 Exemple de modèle Django

Avant d'exécuter le test de création d'objet, vous devez avoir un modèle comme celui-ci :

```python
from django.db import models

class MonModele(models.Model):
    nom = models.CharField(max_length=100)
```

N'oubliez pas de faire une migration :

```bash
python manage.py makemigrations
python manage.py migrate
```

### 📄 À quoi sert le fichier `.dockerignore` ?

Ce fichier fonctionne comme `.gitignore` mais pour Docker. Il empêche Docker de copier certains fichiers dans l'image, comme :
- le dossier `venv/` (inutile dans l'image)
- `.env` (qui contient des secrets)
- `__pycache__/` et fichiers `.pyc` (fichiers de cache inutile)

Cela rend l'image plus légère et plus sécurisée.

### 🔁 GitHub – Initialisation propre

Avant de commencer à pousser votre projet :

1. Créez un dépôt sur https://github.com
2. Dans votre terminal :

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/votre-utilisateur/votre-repo.git
git push -u origin main
```

Ensuite, vous pouvez configurer les Pull Requests et GitHub Actions comme indiqué.