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
DOCKER_IMAGE_STEAM="steam"
DOCKER_CONTAINER_STEAM="steam"
DOCKER_IMAGE_NEOPIXEL="neopixel"
DOCKER_CONTAINER_NEOPIXEL="neopixel"
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

# Controleer of de virtuele omgeving bestaat
if [ ! -d "${VENV_DIR}" ]; then
    echo -e "${YELLOW}Virtuele omgeving bestaat nog niet.. ${YELLOW}Virtuele omgeving configureren${NC}"

    cd ${STEAM_DIR}
    
    # Maak een virtuele omgeving aan
    python -m venv ${VENV_DIR}

    # Kopieer het .env-bestand
    cp .env.example .env

    # Activeer de virtuele omgeving
    source ${VENV_DIR}/bin/activate

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

    # Controleer of de repository bestaat
    if [  -d "${GIT_DIR}" ]; then
        echo -e "${BOLD_GREEN}Repository gevonden${NC}"

     # Controleer of er niet-gecommiteerde wijzigingen zijn
    if [ "$(sudo -u ${REQUIRED_USER} git status --porcelain)" ]; then
        echo -e "${BOLD_YELLOW}Er zijn niet-gecommiteerde wijzigingen.. ${YELLOW}Commit wijzigingen${NC}"
        sudo -u ${REQUIRED_USER} git add . > /dev/null 2>&1
        files=$(sudo -u ${REQUIRED_USER} git status --porcelain | awk '{print $2}')
        sudo -u ${REQUIRED_USER} git commit -m "Update-script: $(date +'%Y-%m-%d %H:%M:%S') - Files: $files"
        sudo -u ${REQUIRED_USER} git push origin $(sudo -u ${REQUIRED_USER} git branch --show-current) 
        echo -e "${BOLD_GREEN}Wijzigingen succesvol gecommit & gepushed: ${files}"
    fi

    # Controleer of de huidige branch de productie-branch is
    if [ "$(sudo -u ${REQUIRED_USER} git branch --show-current)" != "prod_webserv" ]; then
        echo -e "${BOLD_YELLOW}Huidige branch is niet de productie-branch.. ${YELLOW}Overschakelen naar: "origin/prod_webserv"${NC}"
        sudo -u ${REQUIRED_USER} git switch prod_webserv
    fi

        # Controleer of de repository up-to-date is
        sudo -u ${REQUIRED_USER} git pull origin prod_webserv > /dev/null 2>&1

        echo -e "${BOLD_GREEN}Repository is up-to-date${NC}"

    else
        echo -e "${BOLD_RED}Repository niet gevonden${NC}"
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

    # Voeg de gebruiker toe aan de Docker-groep
    sudo usermod -aG docker ${REQUIRED_USER}

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
    if [ "$(sudo docker ps -aq -f name=${DOCKER_CONTAINER_STEAM})" ]; then
        echo -e "${BOLD_YELLOW}Docker-container: ${DOCKER_CONTAINER_STEAM} bestaat al.. ${YELLOW}Container verwijderen..${NC}"

        # Controleer of de Docker-container actief is
        if [ "$(sudo docker ps -q -f name=${DOCKER_CONTAINER_STEAM})" ]; then
            # Stop de Docker-container
            sudo docker stop ${DOCKER_CONTAINER_STEAM}
            echo -e "${GREEN}Oude Docker-container: ${DOCKER_CONTAINER_STEAM} gestopt. ${YELLOW}Verwijder container..${NC}"
        fi

        # Verwijder de Docker-container
        sudo docker rm ${DOCKER_CONTAINER_STEAM}
        echo -e "${GREEN}Oude Docker-container: ${DOCKER_CONTAINER_STEAM} verwijderd${NC}"
    fi

    # Controleer of de Docker-container al bestaat
    if [ "$(sudo docker ps -aq -f name=${DOCKER_CONTAINER_NEOPIXEL})" ]; then
        echo -e "${BOLD_YELLOW}Docker-container: ${DOCKER_CONTAINER_NEOPIXEL} bestaat al.. ${YELLOW}Container verwijderen..${NC}"

        # Controleer of de Docker-container actief is
        if [ "$(sudo docker ps -q -f name=${DOCKER_CONTAINER_NEOPIXEL})" ]; then
            # Stop de Docker-container
            sudo docker stop ${DOCKER_CONTAINER_NEOPIXEL}
            echo -e "${GREEN}Oude Docker-container: ${DOCKER_CONTAINER_AFSTANDSENSOR} gestopt. ${YELLOW}Verwijder container..${NC}"
        fi

        # Verwijder de Docker-container
        sudo docker rm ${DOCKER_CONTAINER_NEOPIXEL}
        echo -e "${GREEN}Oude Docker-container: ${DOCKER_CONTAINER_NEOPIXEL} verwijderd${NC}"
    fi

    # Controleer of het Docker-image bestaat
    if [ "$(sudo docker images -q ${DOCKER_IMAGE_STEAM} )" ]; then
        # Verwijder het Docker-image
        sudo docker image rm ${DOCKER_IMAGE_STEAM}
        echo -e "${GREEN}Oude Docker-image: ${DOCKER_IMAGE_STEAM} verwijderd${NC}"
    fi

    # Controleer of het Docker-image bestaat
    if [ "$(sudo docker images -q ${DOCKER_IMAGE_NEOPIXEL} )" ]; then
        # Verwijder het Docker-image
        sudo docker image rm ${DOCKER_IMAGE_NEOPIXEL}
        echo -e "${GREEN}Oude Docker-image: ${DOCKER_IMAGE_NEOPIXEL} verwijderd${NC}"
    fi

    cd afstandsensor
    sudo docker build -t ${DOCKER_IMAGE_NEOPIXEL} . > /dev/null  2>&1
    echo -e "${BOLD_GREEN}Docker-image: ${DOCKER_IMAGE_NEOPIXEL} succesvol gebouwd${NC}"

    cd ../steam

    # Bouw het Docker-image
    sudo docker build -t ${DOCKER_IMAGE_STEAM} . > /dev/null  2>&1
    echo -e "${BOLD_GREEN}Docker-image: ${DOCKER_IMAGE_STEAM} succesvol gebouwd${NC}"

    # Start de Docker-container
    #sudo docker run -d -p ${DOCKER_PORT}:${DOCKER_PORT} -p ${DOCKER_PORT_SSL}:${DOCKER_PORT_SSL} --privileged --device /dev/gpiomem:/dev/gpiomem --name ${DOCKER_CONTAINER_STEAM} ${DOCKER_IMAGE_STEAM}
    cd docker
    docker compose up -d
    echo -e "${BOLD_GREEN}Docker-container: ${DOCKER_CONTAINER_STEAM} succesvol gestart${NC}"

    echo -e "${BOLD_GREEN}Applicatie is nu beschikbaar op https://${DOCKER_IP}:${DOCKER_PORT_SSL}${NC}"
else 
    echo -e "${BOLD_RED}Dockerfile niet gevonden${NC}"
    exit 1
fi
