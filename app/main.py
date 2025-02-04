import sys
from pathlib import Path
from flask import Flask, make_response, redirect, request, session

basedir = Path(__file__).resolve().parent
sys.path.append(str(basedir.parent))

from app.router.auth import Auth
from app.router.test import Test
from app.router.index import Index
from app.router.dashboard import Dash
from app.router.easteregg import Easter_egg
from app.router.error import page_not_found
from app.connector.babel import babel, get_locale
from app.config import SECRET_KEY, LANGUAGES, BABEL_DEFAULT_LOCALE, BABEL_TRANSLATION_FOLDER


app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config['LANGUAGES'] = LANGUAGES
app.config['BABEL_DEFAULT_LOCALE'] = BABEL_DEFAULT_LOCALE
app.config['BABEL-TRANSLATION-FOLDER'] = str(basedir / BABEL_TRANSLATION_FOLDER)

# Initialiseer hier Flask-extensies
babel.init_app(app, locale_selector=get_locale)

# Foutafhandeling
app.errorhandler(404)(page_not_found)

# Registreer hier blauwdrukken
app.register_blueprint(Index, url_prefix='/')
app.register_blueprint(Dash, url_prefix='/dashboard')
app.register_blueprint(Auth, url_prefix='/auth')
app.register_blueprint(Test, url_prefix='/test')
app.register_blueprint(Easter_egg, url_prefix='/easter-egg')


# Taal wijzigen
@app.route('/change_language/<lang>')
def change_language(lang):
    if lang in app.config['LANGUAGES']:
        response = make_response(redirect(request.referrer))
        response.set_cookie('lang', lang)
        return response
    return redirect(request.referrer)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)