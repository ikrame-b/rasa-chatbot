FROM python:3.10.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Créer un dossier logs pour supervisord
RUN mkdir -p /var/log/supervisor

# Copier la config supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Exposer les ports (5005 = Rasa, 5055 = Actions)
EXPOSE 5005 5055

# Lancer supervisord
CMD ["/usr/bin/supervisord"]
