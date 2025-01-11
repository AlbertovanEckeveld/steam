# Gebruik een bestaande image als basis
FROM python:3.12-slim
LABEL authors="AlbertoVE"

# Installeer de benodigde pakketten en Nginx
RUN apt-get update && apt-get install -y nginx supervisor python3-dev python3-rpi.gpio build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir gunicorn

# Installeer de Python-pakketten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de applicatiecode
COPY . /steam/
COPY .env /steam/.env

# Kopieer configuratiebestanden
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Configureer Nginx
COPY docker/nginx/ssl-default.conf /etc/nginx/sites-available/default
COPY docker/nginx/ssl/certificate.crt /etc/nginx/ssl/certificate.crt
COPY docker/nginx/ssl/private.key /etc/nginx/ssl/private.key

# Zet de werkmap
WORKDIR /steam/app

# Compileer vertalingen
RUN pybabel compile -d translations

# Expose ports
EXPOSE 80 433

# Start Supervisor
CMD ["supervisord", "-n"]
