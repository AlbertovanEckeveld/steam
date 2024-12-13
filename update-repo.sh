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


    
