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

# Stop onmiddellijk als een commando een niet-nul status retourneert
set -e

# Toon de naam van de auteur
echo -e "${BOLD_BLUE}Script gemaakt door Alberto van Eckeveld${NC}"

# Controleer of de repository bestaat
if [ -d ".git" ]; then
    echo -e "${BOLD_GREEN}Repository gevonden${NC}"

    # Controleer of de huidige branch de productie-branch is
    if [ "$(git branch --show-current)" != "prod_webserv" ]; then
        echo -e "${BOLD_YELLOW}Huidige branch is niet de productie-branch.. ${YELLOW}Overschakelen naar: "origin/prod_webserv"${NC}"
        git checkout origin/prod_webserv
    fi

        # Controleer of er niet-gecommiteerde wijzigingen zijn
    if [ "$(git status --porcelain)" ]; then
        echo -e "${BOLD_YELLOW}Er zijn niet-gecommiteerde wijzigingen.. ${YELLOW}Commit wijzigingen${NC}"
        git add .
        files=$(git status --porcelain | awk '{print $2}')
        git commit -m "Update-script: $(date +'%Y-%m-%d %H:%M:%S') - Files: $files"
        git push origin prod_webserv
        echo -e "${GREEN}Wijzigingen succesvol gecommit & gepushed: ${files}"
    fi

    # Controleer of de repository up-to-date is
    git fetch origin prod_webserv

    if [ "$(git rev-parse HEAD)" != "$(git rev-parse @{u})" ]; then
        echo -e "${BOLD_YELLOW}Repository is verouderd, ${YELLOW}nu bijwerken..${NC}"
        
        # Controleer of merge is mogelijk
        if git merge-base @{u} HEAD; then
            git merge origin/prod_webserv
        else
            echo -e "${RED}Merge is niet mogelijk${NC}"
            exit 1
        fi

        echo -e "${GREEN}Repository succesvol bijgewerkt${NC}"

    else
        echo -e "${GREEN}Repository is up-to-date${NC}"
    fi

else
    echo -e "${BOLD_RED}Repository niet gevonden${NC}"
    exit 1
fi


    
