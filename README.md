<p align="center"><img alt="Steam" src="https://img.itch.zone/aW1nLzE4MzUyNzU5LnBuZw==/original/8DRbfb.png" width="260"></p>

# Project Steam - Bitje bij beetje  

Project Steam is een semesterproject binnen de propedeuse van de opleiding HBO-ICT aan de Hogeschool Utrecht.

## Omschrijving
Project Steam is thirt-party platform om gebruikers meer inzicht te geven in hun Steam-spellen en -vrienden.
De Steam Web API is gebruikt om gegevens over spellen en gebruikers op te halen.
 
<details><summary>Context: Opgeleverd prototype</summary><br>

In het opgeleverde prototype van Project Steam is het een webapplicatie, 
die gebruikers in staat stelt om in te loggen met hun Steam-account met RFID Twee-factor authenticatie, 
en hun eigen Steam-profiel, spellen en vrienden te bekijken.
Daarnaast kunnen gebruikers hun spelstatistieken vergelijken met een vriend en de gemiddelde spelprijs per spel-genre bekijken.

###### Technische context
De webapplicatie draaide op een Raspberry Pi 4 met een RFID-lezer en een Oled-display.

Een Raspberry Pi Pico W met een afstands-sensor werd geplaatst boven een beeldscherm, 
om te detecteren of de gebruiker te dicht in de buurt van het beeldscherm zit.

De PostgreSQL database server draaide op een virtual machine in Microsoft Azure.

</details>

## Contributors
<a href="https://github.com/KevinMakkink" target="__blank">![Static Badge](https://img.shields.io/badge/AI:-%20Kevin%20Makkink:%20Kevin%20(1877413)-8A2BE2)</a>
<a href="https://github.com/Remmerswaal" target="__blank">![Static Badge](https://img.shields.io/badge/TI:-%20Max%20Remmerswaal:%20Max%20(1886518)-green)</a> <br>
<a href="https://github.com/Maxbox10" target="__blank">![Static Badge](https://img.shields.io/badge/SD%20UI/UX%20:-%20Max%20Arink:%20MaxBox10%20(1886710)-blue)</a>
<a href="https://github.com/owzezo" target="__blank">![Static Badge](https://img.shields.io/badge/SD%20%20Backend%20:-%20Zaid%20Al%20Abbasy:%20zezo%20(1767972)-blue)</a>
<a href="#">![Static Badge](https://img.shields.io/badge/CSC:-%20Alberto%20van%20Eckeveld:%20AlbertoVE%20(1876166)-yellow)</a>

## Functionaliteiten
- Inloggen met Steam account
- Twee-factor authenticatie met RFID tags
- Gebruikersafstand monitoren met afstands-sensor
- Inzien van eigen Steam-profiel, games en vrienden
- Spel statistieken vergelijken met een vriend
- Gemiddelde spelprijs per spel-genre


## Installatie instructies
### Benodigdheden om de installatiestappen te volgen:
<details><summary>Benodigdheden</summary>

- Git
- Python 3.8 of hoger
- python3-venv
- Database (PostgreSQL)
<br><br>
- (Optioneel) Docker
- (Optioneel) curl
</details>

### Installatie methodes
Er zijn verschillende manieren om de applicatie te installeren en draaien:

<details><summary>Installatie via Docker image (Windows / Linux / MacOS)</summary>

#### Na het clonen van de repository, volg deze stappen om de omgeving op te zetten en de applicatie te draaien in een Docker-container:  

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

<details><summary>Installatie handmatig lokaal (Windows / Linux / MacOS)</summary>

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

<details><summary>Installatie Debian linux script (Linux)</summary>

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

Nadat de applicatie is geïnstalleerd en draait, is de url:  ```http://<ip-adres>:5000/```

## Gebruik

### Vertaling
Om nieuwe vertalingen toe te voegen of bestaande te updaten, volg deze stappen:  

<details><summary>Voeg een nieuwe taal toe aan de configuratie</summary>

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
</details>