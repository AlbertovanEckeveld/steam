from flask import Flask

from app.connector import get_secret_key
from app.router.index import Index
from app.router.authentication import Auth
from app.router.test import Test

def create_app():
    app = Flask(__name__)
    app.secret_key = get_secret_key()

    # Initialize Flask extensions here


    # Register blueprints here
    app.register_blueprint(Index, url_prefix='/')
    app.register_blueprint(Test, url_prefix='/test')
    app.register_blueprint(Auth, url_prefix='/auth')

    return app