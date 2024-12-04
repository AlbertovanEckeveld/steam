import psycopg2
from app.connector import get_database_info, get_user_info

def connect_to_database():
    """
    Establish a connection to the database using the loaded environment variables.
    """
    database = get_database_info()
    credentials = get_user_info()
    try:
        conn = psycopg2.connect(
            host=database['DB_HOST'],
            port=database['DB_PORT'],
            dbname=database['DB_DATABASE'],
            user=credentials['DB_USER'],
            password=credentials['DB_PASSWORD']
        )

        return conn

    except (psycopg2.Error, TypeError) as e:
        print(f"Error connecting to database: {e}")
        raise


def execute_query(query):
    """
    Execute a SQL query on the database connection.
    """
    conn = connect_to_database()
    try:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    except (psycopg2.Error, Exception) as e:
        print(f"Error executing query: {e}")
        raise

def get_version():
    """
    Example function to test the database connection.
    """
    query = """
        SELECT version();
    """
    return execute_query(query)

