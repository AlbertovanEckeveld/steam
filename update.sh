#!/bin/bash

# Auteur: Alberto van Eckeveld
# Datum: 2021-09-29
# Versie: 1.0
# Beschrijving: Dit script update de Steam-applicatie op een Debian-gebaseerd systeem

# Definieer kleurcodes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Geen Kleur

BOLD='\033[1m'
BOLD_RED='\033[1;31m'
BOLD_GREEN='\033[1;32m'
BOLD_YELLOW='\033[1;33m'
BOLD_BLUE='\033[1;34m'
BOLD_NC='\033[0m' # Geen Kleur

# Script informatie
AUTHOR="Alberto van Eckeveld"
REQUIRED_USER="school"
REQUIRED_SCRIPT="update-repo.sh"
VENV_DIR=".venv"
GIT_DIR=".git"
DEBIAN_FILE="/etc/debian_version"

# Docker informatie
DOCKER_IMAGE="steam-project"
DOCKER_CONTAINER="steam-project-prod"
DOCKER_PORT="5000"
DOCKER_IP="192.168.178.248"


# Stop onmiddellijk als een commando een niet-nul status retourneert
set -e

# Toon de naam van de auteur
echo -e "${BOLD_BLUE}Script gemaakt door ${AUTHOR}${NC}"

# Controleer of het script als root wordt uitgevoerd
if [ "$EUID" -ne 0 ]; then
    echo -e "${BOLD_RED}Voer dit script als root uit${NC}"
    exit 1
fi

# Controleer of het systeem Debian-gebaseerd is
if [ -f "${DEBIAN_FILE}" ]; then
    echo -e "${BOLD_GREEN}Systeem is Debian-gebaseerd${NC}"
else
    echo -e "${BOLD_RED}Systeem is niet Debian-gebaseerd${NC}"
    exit 1
fi

# Controleer of de virtuele omgeving bestaat
if [ ! -d "${VENV_DIR}" ]; then
    echo -e "${YELLOW}Virtuele omgeving bestaat nog niet.. ${YELLOW}Virtuele omgeving configureren${NC}"

    cd steam
    
    # Maak een virtuele omgeving aan
    python -m venv .venv

    # Kopieer het .env-bestand
    cp .env.example .env

    # Activeer de virtuele omgeving
    source .venv/bin/activate

    # Installeer de vereiste Python-pakketten
    pip install -r requirements.txt > /dev/null 2>&1 

    # Compileer vertalingen
    pybabel compile -d app/translations

    # Deactiveer de virtuele omgeving
    deactivate

    echo -e "${GREEN}Virtuele omgeving aangemaakt${NC}"
fi
    
# Controleer of git is geinitialiseerd
if [ ! -d "${GIT_DIR}" ]; then
    echo -e "${YELLOW}Git is nog niet geïnitialiseerd"
    exit 1

else
    echo -e "${BOLD_GREEN}Git is geïnitialiseerd${NC}"

    # Update de repository met update-repo.sh script
    if [ -f "${REQUIRED_SCRIPT}" ]; then
        echo -e "${GREEN}${REQUIRED_SCRIPT} script gevonden${NC}"
        sudo -u ${REQUIRED_USER} bash ${REQUIRED_SCRIPT}
    else
        echo -e "${RED}${REQUIRED_SCRIPT} script niet gevonden${NC}"
        exit 1
    fi

fi


# Start de applicatie
echo -e "${BOLD_GREEN}Applicatie starten..${NC}"

# Controleer of Docker al is geïnstalleerd
if [ -x "$(command -v docker)" ]; then
    # Update Docker
    sudo apt-get update > /dev/null 2>&1
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin > /dev/null 2>&1

    echo -e "${GREEN}Docker is al geïnstalleerd en bijgewerkt${NC}"
else 
    echo "Docker is nog niet geïnstalleerd, nu installeren"
    # Voeg de officiële GPG-sleutel van Docker toe:
    sudo apt-get update > /dev/null 2>&1
    sudo apt-get install ca-certificates curl > /dev/null 2>&1
    sudo install -m 0755 -d /etc/apt/keyrings 
    sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Voeg de repository toe aan de Apt-bronnen:
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update > /dev/null 2>&1

    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin > /dev/null 2>&1

    # Start en activeer de Docker-service
    sudo systemctl start docker
    sudo systemctl enable docker

    # Voeg de huidige gebruiker toe aan de Docker-groep
    sudo usermod -aG docker $USER

    echo -e "${GREEN}Docker succesvol geïnstalleerd${NC}"
    echo -e "${GREEN}Docker-service gestart${NC}"
    echo -e "${GREEN}Gebruiker toegevoegd aan de Docker-groep${NC}"
fi

# Controleren of de Docker-service actief is
if [ "$(systemctl is-active docker)" != "active" ]; then
    echo -e "${BOLD_RED}Docker-service is niet actief.. ${YELLOW}Inschakelen ...${NC}"
    sudo systemctl start docker
    echo -e "${GREEN}Docker-service gestart${NC}"
    
fi

# Controleren of de Docker-service is ingeschakeld
if [ "$(systemctl is-enabled docker)" != "enabled" ]; then
    echo -e "${BOLD_RED}Docker-service is niet ingeschakeld.. ${YELLOW}Inschakelen ...${NC}"
    sudo systemctl enable docker
    echo -e "${GREEN}Docker-service ingeschakeld${NC}"
fi

# Controleer of er een Dockerfile aanwezig is
if [ -f "Dockerfile" ]; then

    # Controleer of de Docker-container al bestaat
    if [ "$(sudo docker ps -aq -f name=steam-project-prod)" ]; then
        echo -e "${BOLD_YELLOW}Docker-container bestaat al.. ${YELLOW}Container verwijderen..${NC}"
        
        # Controleer of de Docker-container actief is
        if [ "$(sudo docker ps -q -f name=steam-project-prod)" ]; then
            # Stop de Docker-container
            sudo docker stop steam-project-prod
            echo -e "${GREEN}Oude Docker-container gestopt. ${YELLOW}Verwijder container..${NC}"
        fi

        # Verwijder de Docker-container
        sudo docker rm steam-project-prod
        echo -e "${GREEN}Oude Docker-container verwijderd${NC}"
    fi

    # Controleer of het Docker-image bestaat
    if [ "$(sudo docker images -q steam-project)" ]; then
        # Verwijder het Docker-image
        sudo docker rmi steam-project
        echo -e "${GREEN}Oude Docker-image verwijderd${NC}"
    fi

    # Bouw het Docker-image
    sudo docker build -t ${DOCKER_IMAGE} . > /dev/null  2>&1 
    echo -e "${BOLD_GREEN}Docker-image succesvol gebouwd${NC}"

    # Start de Docker-container
    sudo docker run -d -p 5000:5000 --name ${DOCKER_CONTAINER} ${DOCKER_IMAGE}
    echo -e "${BOLD_GREEN}Docker-container succesvol gestart${NC}"
    echo -e "${BOLD_GREEN}Docker container aangemaakt met de naam ${DOCKER_CONTAINER}$, met poort: ${DOCKER_PORT}{NC}"
    echo -e "${BOLD_GREEN}Applicatie is nu beschikbaar op http://${DOCKER_IP}:${DOCKER_PORT}${NC}"
else 
    echo -e "${BOLD_RED}Dockerfile niet gevonden${NC}"
    exit 1
fi