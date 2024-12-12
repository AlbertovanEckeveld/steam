# Gebruik een officiële Python runtime als parent image
FROM python:3.9-slim
LABEL authors="alberto"

# Stel de werkdirectory in in de container
WORKDIR /app

# Kopieer de requirements file naar de werkdirectory
COPY requirements.txt .

# Installeer de Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de rest van de applicatiecode naar de werkdirectory
COPY . .

CMD ["pybabel", "compile", "-d", "app/translations"]

# Stel de environment variables in
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Exposeer de poort waarop de app draait
EXPOSE 5000

# Definieer het commando om de app te starten
CMD ["flask", "run", "--host=0.0.0.0"]