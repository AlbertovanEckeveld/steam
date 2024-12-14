![Steam](https://logos-world.net/wp-content/uploads/2020/10/Steam-Logo-2002-present.png) 

# Project Steam - Bitje bij beetje 🚀
![Static Badge](https://img.shields.io/badge/AI:-%20Kevin%20Makkink:%20Kevin%20(1877413)-8A2BE2)  <br> 
![Static Badge](https://img.shields.io/badge/TI:-%20Max%20Remmerswaal:%20Max%20(1886518)-8A2BE2) <br>
![Static Badge](https://img.shields.io/badge/SD%20(Backend):-%20Zaid%20Al%20Abbasy:%20zezo%20(1767972)-8A2BE2) <br> 
![Static Badge](https://img.shields.io/badge/SD(Frontend):-%20Max%20Arink:%20MaxBox10%20(1886710)-8A2BE2) <br> 
![Static Badge](https://img.shields.io/badge/CSC:-%20Alberto%20van%20Eckeveld:%20AlbertoVE%20(1876166)-8A2BE2) <br>

## Omschrijving
Project Steam is bedoeld om gebruikers meer inzicht te geven in hun Steam-games en -vrienden.
De Steam Web API is gebruikt om gegevens over games en gebruikers op te halen.
Project Steam is een webapplicatie geschreven in Python met behulp van het Flask framework. 

## Installatie instructies
Er zijn verschillende manieren om de applicatie te installeren en draaien, zowel lokaal als in een Docker-container.

<details><summary>Installatie via Docker image</summary>

#### Na het clonen van de repository, volg deze stappen om de omgeving op te zetten en de applicatie te draaien
in een Docker-container:  

#### Bouw de Docker image:  
```sh
docker build -t steam-project .
```
#### Draai de Docker container:  
```sh
docker run -d -p 5000:5000 --name steam-project--prod steam-project
```
Met deze instructies kun je de applicatie eenvoudig opzetten en draaien, zowel lokaal als in een Docker-container.

</details>

<details><summary>Installatie handmatig lokaal</summary>

#### Na het clonen van de repository, volg deze stappen om de omgeving op te zetten en de applicatie lokaal te draaien:

#### 1: Maak een virtuele omgeving aan:
```sh
   python -m venv .venv
```

#### 2: Activeer de virtuele omgeving:  
Voor Linux/macOS:
```sh
source .venv/bin/activate
```
Voor Windows:
```sh
.venv\Scripts\activate
```
#### 3: Installeer de vereiste Python-pakketten:  
```sh
pip install -r requirements.txt
```
#### 4: Compileer de vertalingen:  
```sh
pybabel compile -d app/translations
```
#### 5: Start de Flask-applicatie:  
```sh
flask run --host=0.0.0.0 --debug
```
Met deze stappen kun je de applicatie lokaal opzetten en draaien.

</details>

<details><summary>Installatie Debian linux script</summary>

#### Er is een installatie script beschikbaar voor ***Debian Systemen*** om de applicatie eenvoudig op te zetten en draaien in docker.
Om de applicatie te installeren en draaien, volg deze stappen om het installatie script te downloaden en uit te voeren:

#### 1: Instaleer eerst het installatie script:
```sh
curl -L  https://raw.githubusercontent.com/AlbertovanEckeveld/steam/refs/heads/main/setup.sh?token=GHSAT0AAAAAAC3TTZVNSOQX3KYJJ3R2DSBGZ23OKPA -o setup.sh
```
#### 2: Maak het script uitvoerbaar en voer het uit:
```sh
sudo chmod a+x setup.sh && sudo ./setup.sh
```
</details>

### Vertaling
Om nieuwe vertalingen toe te voegen of bestaande te updaten, volg deze stappen:  

#### Extraheer de vertaalbare strings: 
```sh
pybabel extract -F babel.cfg -o messages.pot .
```
#### Initialiseer de vertaling voor een nieuwe taal (bijvoorbeeld Engels): 
```sh
pybabel init -i messages.pot -d app/translations -l en
```
#### Compileer de vertalingen:  
```sh
pybabel compile -d app/translations
```
