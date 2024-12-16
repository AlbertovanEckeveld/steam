#!/bin/bash

# Auteur: Alberto van Eckeveld
# Datum: 2021-09-29
# Versie: 1.0
# Beschrijving: Dit script installeert en configureert de Steam-applicatie op een Debian-gebaseerd systeem

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
STEAM_DIR="steam"
DEBIAN_FILE="/etc/debian_version"

# Docker informatie
DOCKER_IMAGE="steam"
DOCKER_CONTAINER="steam"
DOCKER_PORT="80"
DOCKER_PORT_SSL="443"
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

# Controleer of de repository nog niet is gekloond
if [ ! -d ${STEAM_DIR} ]; then
    echo -e "${YELLOW}Repository nog niet gekloond, nu klonen..${NC}"

    # Controleer of Python3 is geïnstalleerd
    if [ ! -x "$(command -v python3)" ]; then
        echo -e "${YELLOW}Python3 is niet geïnstalleerd, installeren...${NC}"
        sudo apt-get update && sudo apt-get upgrade -y > /dev/null 2>&1
        sudo apt-get install -y python3 python3-venv python3-pip python3-dev build-essential gettext git > /dev/null 2>&1
    fi

    # Kloon de repository
    sudo -u ${REQUIRED_USER} git clone git@github.com:AlbertovanEckeveld/steam.git > /dev/null 2>&1
    echo -e "${GREEN}Repository succesvol gekloond${NC}"
    
else 
    echo -e "${GREEN}Repository is al gekloond${NC}"
fi

# Controleer of de repository succesvol is gekloond en controleer het bestaan van virtuele omgeving
if [ -d "${STEAM_DIR}" ]; then

    cd ${STEAM_DIR}

    # Controleer of de repository bestaat
    if [  -d "${GIT_DIR}" ]; then
        echo -e "${BOLD_GREEN}Repository gevonden${NC}"

        # Controleer of de huidige branch de productie-branch is
        if [ "$(sudo -u ${REQUIRED_USER} git branch --show-current)" != "prod_webserv" ]; then
            echo -e "${BOLD_YELLOW}Huidige branch is niet de productie-branch.. ${YELLOW}Overschakelen naar: origin/prod_webserv${NC}"
            sudo -u ${REQUIRED_USER} git switch origin/prod_webserv
        fi

        # Controleer of de repository up-to-date is
        sudo -u ${REQUIRED_USER} git pull origin prod_webserv > /dev/null 2>&1

        sudo chmod a+x ${REQUIRED_SCRIPT}
        sudo chmod a+x update.sh

    fi

    # Controleer of de virtuele omgeving bestaat
    if [ ! -d ${VENV_DIR} ]; then
        echo -e "${YELLOW}Virtuele omgeving bestaat nog niet.. ${YELLOW}Virtuele omgeving configureren${NC}"

        # Maak een virtuele omgeving aan
        python -m venv ${VENV_DIR}

        # Kopieer het .env-bestand
        cp .env.example .env

        # Activeer de virtuele omgeving
        source ${VENV_DIR}/bin/activate

        # Installeer de vereiste Python-pakketten
        pip install -r requirements.txt > /dev/null 2>&1 

        # Compileer vertalingen
        pybabel compile -d app/translations > /dev/null 2>&1

        # Deactiveer de virtuele omgeving
        deactivate

        echo -e "${GREEN}Virtuele omgeving aangemaakt${NC}"
    fi
    
fi

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

    # Voeg de gebruiker toe aan de Docker-groep
    sudo usermod -aG docker ${REQUIRED_USER}

    echo -e "${GREEN}Docker succesvol geïnstalleerd${NC}"
    echo -e "${GREEN}Docker-service gestart${NC}"
    echo -e "${GREEN}Gebruiker: ${REQUIRED_USER} toegevoegd aan de Docker-groep${NC}"
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

# Controleer of de working directory de steam-map is
if [ "$(basename "$PWD")" != "steam" ]; then
    cd ${STEAM_DIR}
fi

# Controleer of er een Dockerfile aanwezig is
if [ -f "Dockerfile" ]; then

    # Controleer of de Docker-container al bestaat
    if [ "$(sudo docker ps -aq -f name=${DOCKER_CONTAINER})" ]; then
        echo -e "${BOLD_YELLOW}Docker-container: ${DOCKER_CONTAINER} bestaat al.. ${YELLOW}Container verwijderen..${NC}"
        
        # Controleer of de Docker-container actief is
        if [ "$(sudo docker ps -q -f name=${DOCKER_CONTAINER})" ]; then
            # Stop de Docker-container
            sudo docker stop ${DOCKER_CONTAINER}
            echo -e "${GREEN}Oude Docker-container: ${DOCKER_CONTAINER} gestopt. ${YELLOW}Verwijder container..${NC}"
        fi

        # Verwijder de Docker-container
        sudo docker rm ${DOCKER_CONTAINER}
        echo -e "${GREEN}Oude Docker-container: ${DOCKER_CONTAINER} verwijderd${NC}"
    fi

    # Controleer of het Docker-image bestaat
    if [ "$(sudo docker images -q ${DOCKER_IMAGE} )" ]; then
        # Verwijder het Docker-image
        sudo docker image rm ${DOCKER_IMAGE}
        echo -e "${GREEN}Oude Docker-image: ${DOCKER_IMAGE} verwijderd${NC}"
    fi

    # Bouw het Docker-image
    sudo docker build -t ${DOCKER_IMAGE} . > /dev/null  2>&1 
    echo -e "${BOLD_GREEN}Docker-image: ${DOCKER_IMAGE} succesvol gebouwd${NC}"

    # Start de Docker-container
    sudo docker run -d -p ${DOCKER_PORT}:${DOCKER_PORT} -p ${DOCKER_PORT_SSL}:${DOCKER_PORT_SSL} --name ${DOCKER_CONTAINER} ${DOCKER_IMAGE}
    echo -e "${BOLD_GREEN}Docker-container: ${DOCKER_CONTAINER} succesvol gestart${NC}"

    echo -e "${BOLD_GREEN}Applicatie is nu beschikbaar op https://${DOCKER_IP}:${DOCKER_PORT_SSL}${NC}"
else 
    echo -e "${BOLD_RED}Dockerfile niet gevonden${NC}"
    exit 1
fi
