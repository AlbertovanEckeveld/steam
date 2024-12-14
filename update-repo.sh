#!/bin/bash

# Auteur: Alberto van Eckeveld
# Datum: 2021-09-29
# Versie: 1.0
# Beschrijving: Dit script update de Steam-applicatie code op een Debian-gebaseerd systeem

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

# Stop onmiddellijk als een commando een niet-nul status retourneert
set -e

# Controleer of het systeem Debian-gebaseerd is
if [ ! -f "${DEBIAN_FILE}" ]; then
    echo -e "${BOLD_RED}Systeem is niet Debian-gebaseerd${NC}"
    exit 1
fi

# Controleer of de repository bestaat
if [  -d "${GIT_DIR}" ]; then
    echo -e "${BOLD_GREEN}Repository gevonden${NC}"

    # Controleer of de huidige branch de productie-branch is
    if [ "$(sudo -u ${REQUIRED_USER} git branch --show-current)" != "prod_webserv" ]; then
        echo -e "${BOLD_YELLOW}Huidige branch is niet de productie-branch.. ${YELLOW}Overschakelen naar: "origin/prod_webserv"${NC}"
        sudo -u ${REQUIRED_USER} git checkout origin/prod_webserv
        sudo -u ${REQUIRED_USER} git add . > /dev/null 2>&1
        sudo -u ${REQUIRED_USER} git commit -m "Update-script: $(date +'%Y-%m-%d %H:%M:%S') - Files: $(sudo -u ${REQUIRED_USER} git status --porcelain | awk '{print $2}')"
        sudo -u ${REQUIRED_USER} git push origin $(sudo -u ${REQUIRED_USER} git branch --show-current)
        sudo -u ${REQUIRED_USER} git checkout origin/prod_webserv
    fi

    # Controleer of er niet-gecommiteerde wijzigingen zijn
    if [ "$(sudo -u ${REQUIRED_USER} git status --porcelain)" ]; then
        echo -e "${BOLD_YELLOW}Er zijn niet-gecommiteerde wijzigingen.. ${YELLOW}Commit wijzigingen${NC}"
        sudo -u ${REQUIRED_USER} git add . > /dev/null 2>&1
        files=$(sudo -u ${REQUIRED_USER} git status --porcelain | awk '{print $2}')
        sudo -u ${REQUIRED_USER} git commit -m "Update-script: $(date +'%Y-%m-%d %H:%M:%S') - Files: $files"
        sudo -u ${REQUIRED_USER} git push origin prod_webserv 
        echo -e "${BOLD_GREEN}Wijzigingen succesvol gecommit & gepushed: ${files}"
    fi

    # Controleer of de repository up-to-date is
    sudo -u ${REQUIRED_USER} git pull origin/prod_webserv > /dev/null 2>&1

    if [ "$(sudo -u ${REQUIRED_USER} git rev-parse HEAD)" != "$(sudo -u ${REQUIRED_USER} git rev-parse @{u})" ]; then
        echo -e "${BOLD_YELLOW}Repository is verouderd, ${YELLOW}nu bijwerken..${NC}"
        
        # Controleer of merge is mogelijk
        if sudo -u ${REQUIRED_USER} git merge-base @{u} HEAD; then
            sudo -u ${REQUIRED_USER} git merge origin/prod_webserv
        else
            echo -e "${RED}Merge is niet mogelijk${NC}"
            exit 1
        fi

        echo -e "${GREEN}Repository succesvol bijgewerkt${NC}"

    else
        echo -e "${GREEN}Repository was al up-to-date${NC}"
    fi

    echo -e "${BOLD_GREEN}Repository is up-to-date${NC}"

else
    echo -e "${BOLD_RED}Repository niet gevonden${NC}"
    exit 1
fi


    
