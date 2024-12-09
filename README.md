# Project Steam - Bitje bij beetje 🚀

![Steam](https://logos-world.net/wp-content/uploads/2020/10/Steam-Logo-2002-present.png) 

## Probeer alles te doen via een Commit
Welkom bij ons innovatieve project waarin onze startup het Steam-platform gaat ondersteunen en uitbreiden. Ons team van vijf studenten gaat aan de slag om Steam te helpen met het verbeteren van gebruikerservaringen door inzichten te bieden in gaming-gedrag via nieuwe, interactieve dashboards en grafische weergaven.


Vertaling:
pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d app/translations -l en
pybabel compile -d app/translations
