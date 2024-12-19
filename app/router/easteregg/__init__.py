from flask import Blueprint, render_template

from app.connector.rfid import tfa

# Auth blueprint
Easter_egg = Blueprint('easter-egg', __name__, static_folder='app/static', template_folder='app/templates')

@Easter_egg.route('/')
def index():
    """
        Index route voor easter eggs.

        Returns:
        Response: Redirect naar de pagina voor easter eggs.
    """

    if tfa() == True:
        # Redirect naar de easter eggs pagina
        return render_template("easter-egg/Easter_egg-jeroen.html")


@Easter_egg.route('/alberto')
def alberto():
    """
        Alberto route easter egg.

        Returns:
        Response: Redirect naar de alberto pagina voor easter egg.
    """

    if tfa() == True:
    # Redirect naar de easter eggs pagina
        return render_template("easter-egg/Easter_egg-alberto.html")

