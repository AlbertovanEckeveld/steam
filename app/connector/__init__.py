from app.config import DB_HOST, DB_PORT, DB_DATABASE, DB_USER, DB_PASSWORD, SECRET_KEY, STEAM_API_KEY

def get_database_info():
    """
    Load database info variables from .env file.
    """
    return {
        'DB_HOST': DB_HOST,
        'DB_PORT': DB_PORT,
        'DB_DATABASE': DB_DATABASE
    }

def get_user_info():
    """
    Load user info variables from .env file.
    """
    return {
        'DB_USER': DB_USER,
        'DB_PASSWORD': DB_PASSWORD
    }

def get_steam_API():
    """
    Load steam api variables from .env file.
    """
    return STEAM_API_KEY

def get_secret_key():
    """
    Load secret key variables from .env file.
    """
    return SECRET_KEY