<p align="center"><img alt="Steam" src="https://img.itch.zone/aW1nLzE4MzUyNzU5LnBuZw==/original/8DRbfb.png" width="200"></p>

# Project Steam - Bitje bij beetje  

Project Steam is een semesterproject binnen de propedeuse van de opleiding HBO-ICT aan de Hogeschool Utrecht.

## Omschrijving
Project Steam is third-party platform om gebruikers meer inzicht te geven in hun Steam spellen en vrienden.
De Steam Web API is gebruikt om gegevens van spellen en gebruikers op te halen.
 
<details><summary>Context: Opgeleverd prototype</summary><br>

Het opgeleverde prototype van Project Steam is een webapplicatie.
Deze webapplicatie biedt de volgende mogelijkheden:
- Inloggen via Steam
- 2FA doormiddel van een RFID tag
- Je eigen Steamprofiel bekijken
- Het Steamprofiel van vrienden bekijken
- Speeltijd bekijken en vergelijken
- Multi-language support


###### Technische context
- De webapplicatie draaide op een Raspberry Pi 4 in een docker container met een RFID-lezer, een HC-SR04 afstandsensor en een NeoPixel.
- De PostgreSQL database server draaide op een virtual machine in Microsoft Azure en lokaal op de Raspberry Pi met een replicatie.

</details>

## Contributors
<a href="https://github.com/KevinMakkink" target="__blank">![Static Badge](https://img.shields.io/badge/AI:-%20Kevin%20Makkink:%20Kevin%20(1877413)-8A2BE2)</a>
<a href="https://github.com/Remmerswaal" target="__blank">![Static Badge](https://img.shields.io/badge/TI:-%20Max%20Remmerswaal:%20Max%20(1886518)-green)</a> <br>
<a href="https://github.com/Maxbox10" target="__blank">![Static Badge](https://img.shields.io/badge/SD%20UI/UX:-%20Max%20Arink:%20MaxBox10%20(1886710)-blue)</a>
<a href="https://github.com/owzezo" target="__blank">![Static Badge](https://img.shields.io/badge/SD%20%20Backend:-%20Zaid%20Al%20Abbasy:%20zezo%20(1767972)-blue)</a>
<a href="#">![Static Badge](https://img.shields.io/badge/CSC%20en%20SD%20backend:-%20Alberto%20van%20Eckeveld:%20AlbertoVE%20(1876166)-yellow)</a>

## Functionaliteiten
- Inloggen met Steam account
- 2FA met RFID tags
- Gebruikersafstand monitoren met afstands-sensor (HC-SR04)
- Inzien van eigen Steam-profiel, games en vrienden
- Spel statistieken vergelijken met een vriend


## Showcase
Check here for the demo:
[steam.albertove.nl](https://steam.albertove.nl)


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
