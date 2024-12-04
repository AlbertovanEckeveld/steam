import os
from dotenv import load_dotenv

def get_database_info():
    """
    Load database info variables from .env file.
    """
    load_dotenv()
    return {
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'DB_DATABASE': os.getenv('DB_DATABASE')
    }

def get_user_info():
    """
    Load user info variables from .env file.
    """
    load_dotenv()
    return {
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD')
    }

def get_steam_API():
    """
    Load steam api variables from .env file.
    """
    load_dotenv()
    return os.getenv('STEAM_API')