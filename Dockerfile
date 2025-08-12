# Utilise une image Python de base légère
FROM python:3.10-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier des dépendances et les installe
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le reste du code de l'application
COPY . .

# Expose le port 8000, utilisé par le serveur de développement Django
EXPOSE 8000

# Lance le serveur de développement
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]