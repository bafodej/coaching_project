# Image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Commande pour lancer l'application Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]