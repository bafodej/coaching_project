# 🏋️ Coaching Project - Application de Gestion de Séances

Application Django pour la gestion de rendez-vous de coaching sportif.

[![Django CI](https://github.com/bafodej/coaching_project/actions/workflows/django-ci.yml/badge.svg)](https://github.com/bafodej/coaching_project/actions/workflows/django-ci.yml)

## 📋 Description

Application web permettant aux coachs sportifs de gérer leurs séances avec leurs clients. Les fonctionnalités incluent la prise de rendez-vous, le suivi des séances et la gestion des notes de coaching.

## 🏗️ Structure du Projet
```
coaching_project/
├── appointments/           # Application principale de gestion des séances
│   ├── migrations/        # Migrations de base de données
│   ├── templates/         # Templates HTML
│   │   ├── appointments/  # Templates des rendez-vous
│   │   └── registration/  # Templates d'authentification
│   ├── admin.py          # Configuration admin Django
│   ├── forms.py          # Formulaires
│   ├── models.py         # Modèles de données
│   ├── tests.py          # Tests unitaires
│   ├── urls.py           # URLs de l'app
│   └── views.py          # Vues
├── coaching_site/         # Configuration du projet Django
│   ├── settings.py       # Paramètres Django
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuration WSGI
├── theme/                 # Application Tailwind CSS
├── .github/
│   └── workflows/
│       └── django-ci.yml  # Pipeline CI/CD
├── .flake8               # Configuration Flake8
├── requirements.txt      # Dépendances Python
├── manage.py             # Script de gestion Django
└── README.md             # Ce fichier
```

## 🚀 Technologies

- **Backend** : Django 5.0.6
- **Frontend** : Tailwind CSS (django-tailwind)
- **Base de données** : SQLite (dev)
- **Linting** : Flake8
- **CI/CD** : GitHub Actions

## 📦 Installation

### Prérequis

- Python 3.9+
- pip

### Étapes

1. **Cloner le repository**
```bash
git clone https://github.com/bafodej/coaching_project.git
cd coaching_project
```

2. **Créer un environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Appliquer les migrations**
```bash
python manage.py migrate
```

5. **Créer un superutilisateur (optionnel)**
```bash
python manage.py createsuperuser
```

6. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

L'application sera accessible sur `http://127.0.0.1:8000/`

## 🧪 Tests

Pour lancer les tests unitaires :
```bash
python manage.py test appointments
```

Pour vérifier la qualité du code avec Flake8 :
```bash
flake8 .
```

Couverture actuelle : **6 tests unitaires**

## 📊 Modèle de Données

### Seance
Représente une séance de coaching entre un coach et un client.

**Champs :**
- `client` : Utilisateur (ForeignKey vers User)
- `date` : Date du rendez-vous (DateField)
- `heure_debut` : Heure de début (TimeField)
- `objet` : Objet de la séance (CharField)
- `duree` : Durée en minutes - 60, 90 ou 120 (IntegerField)
- `notes_coach` : Notes privées du coach (TextField, optionnel)
- `cree_le` : Date de création (auto)
- `modifie_le` : Date de modification (auto)

**Méthodes :**
- `heure_fin` : Calcule automatiquement l'heure de fin
- `clean()` : Validation métier (empêche les RDV dans le passé)

**Contraintes :**
- Un client ne peut pas avoir 2 RDV au même moment (unique_together)

## 🔄 CI/CD

Le projet utilise GitHub Actions pour l'intégration continue :

**Pipeline automatique à chaque push/PR :**
1. ✅ **Linting** : Vérification de la qualité du code avec Flake8
2. ✅ **Tests** : Exécution de tous les tests unitaires Django

**Workflow** : `.github/workflows/django-ci.yml`

## 👨‍💻 Auteur

**Bafodé** - 


## 📝 Licence

Ce projet est à but éducatif.
