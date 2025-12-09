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
# Utilise le port défini par azure via $PORT , ou 8000 par défaut 
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:${PORT:-8000}"]