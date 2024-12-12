

![Steam](https://logos-world.net/wp-content/uploads/2020/10/Steam-Logo-2002-present.png) 

# Project Steam - Bitje bij beetje 🚀
Welkom bij ons innovatieve project waarin onze startup het Steam-platform gaat ondersteunen en uitbreiden. Ons team van vijf studenten gaat aan de slag om Steam te helpen met het verbeteren van gebruikerservaringen door inzichten te bieden in gaming-gedrag via nieuwe, interactieve dashboards en grafische weergaven.


## Installatie instructies

Na het clonen van de repository, volg deze stappen om de omgeving op te zetten en de applicatie te draaien:

## Installatie script

Instaleer eerst het installatie script:
```sh
   wget https://raw.githubusercontent.com/AlbertovanEckeveld/steam/refs/heads/main/setup.sh?token=GHSAT0AAAAAAC3TTZVNSOQX3KYJJ3R2DSBGZ23OKPA
```
Maak het script executable:
```sh
   sudo chmod a+x setup.sh
```
Clone het project:
```sh
   git clone https://github.com/AlbertovanEckeveld/steam.git
```
Voer het script vervolgens uit:
```sh
   sudo ./setup.sh
```


## Docker
Om de applicatie in een Docker-container te draaien, volg deze stappen:  

### Bouw de Docker image:  
```sh
docker build -t steam-project .
```
### Draai de Docker container:  
```sh
docker run -d -p 5000:5000 --name steam-project--prod steam-project
```
Met deze instructies kun je de applicatie eenvoudig opzetten en draaien, zowel lokaal als in een Docker-container.

## Handmatig lokaal

### 1. Maak een virtuele omgeving aan:
```sh
   python -m venv .venv
```

### 2. Activeer de virtuele omgeving:  
Voor Linux/macOS:
```sh
source .venv/bin/activate
```
Voor Windows:
```sh
.venv\Scripts\activate
```
### 3. Installeer de vereiste Python-pakketten:  
```sh
pip install -r requirements.txt
```
### 4. Compileer de vertalingen:  
```sh
pybabel compile -d app/translations
```
### 5. Start de Flask-applicatie:  
```sh
flask run --host=0.0.0.0 --debug
```
Met deze stappen kun je de applicatie lokaal opzetten en draaien.

## Vertaling
Vertaling
Om nieuwe vertalingen toe te voegen of bestaande te updaten, volg deze stappen:  
Extraheer de vertaalbare strings: 
```sh
pybabel extract -F babel.cfg -o messages.pot .
```
Initialiseer de vertaling voor een nieuwe taal (bijvoorbeeld Engels): 
```sh
pybabel init -i messages.pot -d app/translations -l en
```
Compileer de vertalingen:  
```sh
pybabel compile -d app/translations
```