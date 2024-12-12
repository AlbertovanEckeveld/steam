from flask_babel import Babel
from flask import request

def get_locale():
    return request.cookies.get('lang')

babel = Babel()
