import os
import psycopg2
from dotenv import load_dotenv

def load_environment_variables():
    """
    Load environment variables from .env file.
    """
    load_dotenv()
    return {
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'DB_DATABASE': os.getenv('DB_DATABASE'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD')
    }


def connect_to_database():
    """
    Establish a connection to the database using the loaded environment variables.
    """
    env_vars = load_environment_variables()
    try:
        conn = psycopg2.connect(
            host=env_vars['DB_HOST'],
            port=env_vars['DB_PORT'],
            dbname=env_vars['DB_DATABASE'],
            user=env_vars['DB_USER'],
            password=env_vars['DB_PASSWORD']
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

def get_customers():
    """
    Example function to test the database connection.
    """
    query = """
        SELECT * FROM test;
    """
    return execute_query(query)


def main():
    print(get_customers())


if __name__ == '__main__':
    main()