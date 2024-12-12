from app.config import DB_HOST, DB_PORT, DB_DATABASE, DB_USER, DB_PASSWORD, STEAM_API_KEY, address

def get_database_info():
    """
        Laad databaseinformatie variabelen uit het bestand config.py.
    """
    return {
        'DB_HOST': DB_HOST,
        'DB_PORT': DB_PORT,
        'DB_DATABASE': DB_DATABASE
    }

def get_user_info():
    """
        Laad gebruikersinformatie variabelen uit het bestand config.py.
    """
    return {
        'DB_USER': DB_USER,
        'DB_PASSWORD': DB_PASSWORD
    }

def get_address():
    """
        Laad IPv4-adres variabelen uit het bestand config.py.
    """
    return address

def get_steam_API():
    """
        Laad Steam API-sleutel variabel uit het bestand config.py.
    """
    return STEAM_API_KEY
