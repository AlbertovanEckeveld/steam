import psycopg2
from psycopg2 import sql

from app.connector import get_database_info, get_user_info

def connect_to_database():
    """
        Maak verbinding met de database met behulp van de geladen omgevingsvariabelen.

        Returns:
            obj: psycopg2-verbinding met de database.
    """
    # Haal database-informatie en gebruikersinformatie op
    database = get_database_info()
    credentials = get_user_info()

    try:
        # Maak verbinding met de database
        conn = psycopg2.connect(
            host=database['DB_HOST'],
            port=database['DB_PORT'],
            dbname=database['DB_DATABASE'],
            user=credentials['DB_USER'],
            password=credentials['DB_PASSWORD']
        )
        return conn

    except (psycopg2.Error, TypeError) as e:
        # Print foutmelding
        print(f"Fout bij het verbinden met de database: {e}")
        raise


def execute_query(query, params=None):
    """
        Voer een SQL-query uit op de databaseverbinding.

        Argumenten:
            query (str): De uit te voeren SQL-query.
            params (tuple, optioneel): Parameters om mee te geven aan de query.

        Returns:
            list: Queryresultaten.
    """
    # Maak verbinding met de database
    conn = connect_to_database()
    try:
        # Voer de query uit met behulp van een cursor
        with conn.cursor() as cur:
            cur.execute(sql.SQL(query), params)
            results = cur.fetchall()
        # Commit de transactie
        conn.commit()
        return results
    except (psycopg2.Error, Exception) as e:
        # Print foutmelding, rol de transactie terug en gooi de fout opnieuw
        print(f"Fout bij het uitvoeren van de query: {e}")
        conn.rollback()
        raise
    finally:
        # Sluit de databaseverbinding
        conn.close()

def get_version():
    """
        Voorbeeldfunctie om de databaseverbinding te testen.

        Returns:
            list: Databaseversie.
    """
    query = """
        SELECT version();
    """
    return execute_query(query)

