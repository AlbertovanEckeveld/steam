from flask import Flask

from app.views.index import Index
from app.views.test import Test

from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here
    app.register_blueprint(Index, url_prefix='/')
    app.register_blueprint(Test, url_prefix='/test')

    return app