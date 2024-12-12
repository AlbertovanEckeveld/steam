from app.initialize import env_vars

DB_HOST                         = env_vars.get('DB_HOST')
DB_PORT                         = env_vars.get('DB_PORT')
DB_USER                         = env_vars.get('DB_USER')
DB_PASSWORD                     = env_vars.get('DB_PASSWORD')
DB_DATABASE                     = env_vars.get('DB_DATABASE')

ADDRESS                         = env_vars.get('ADDRESS')
SECRET_KEY                      = env_vars.get('SECRET_KEY')
STEAM_API_KEY                   = env_vars.get('STEAM_API')

LANGUAGES                       = ['en', 'nl']
BABEL_DEFAULT_LOCALE            = 'nl'
BABEL_TRANSLATION_FOLDER        = 'translations'