from flask import Flask

from app.router.index import Index
from app.router.login import Login
from app.router.test import Test

def create_app():
    app = Flask(__name__)

    # Initialize Flask extensions here


    # Register blueprints here
    app.register_blueprint(Index, url_prefix='/')
    app.register_blueprint(Test, url_prefix='/test')
    app.register_blueprint(Login, url_prefix='/login')

    return app