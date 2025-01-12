# Gebruik een bestaande image als basis
FROM python:3.12-slim
LABEL authors="AlbertoVE"

# Installeer de benodigde pakketten en Nginx
RUN apt-get update && apt-get install -y python3-dev python3-rpi.gpio build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# Installeer de Python-pakketten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de applicatiecode
COPY . /afstandsensor/

# Zet de werkmap
WORKDIR /afstandsensor/

CMD ["python3", "main.py"]