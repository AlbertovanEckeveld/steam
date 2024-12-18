# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies and Nginx
RUN apt-get update && apt-get install -y nginx supervisor && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN sudo apt install --no-cache-dir python3-full
RUN sudo apt install python3-rpi.gpio
RUN pip install --no-cache-dir gunicorn

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /steam/

# Copy configuration files 
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set up Nginx
COPY docker/nginx/ssl-default.conf /etc/nginx/sites-available/default
COPY docker/nginx/ssl/certificate.crt /etc/nginx/ssl/certificate.crt
COPY docker/nginx/ssl/private.key /etc/nginx/ssl/private.key

# Set working directory
WORKDIR /steam/app

# Compile translations
RUN pybabel compile -d translations

# Expose ports
EXPOSE 80 433

# Start Supervisor
CMD ["supervisord", "-n"]