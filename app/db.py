import os
import pyodbc
from dotenv import load_dotenv

def load_environment_variables():
    """
    Load environment variables from .env file.
    """
    load_dotenv()
    return {
        'DB_HOST': os.getenv('DB_HOST'),
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
        conn_string = (f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                       f"SERVER={env_vars['DB_HOST']};"
                       f"DATABASE={env_vars['DB_DATABASE']};"
                       f"UID={env_vars['DB_USER']};"
                       f"PWD={env_vars['DB_PASSWORD']}")

        conn = pyodbc.connect(conn_string)
        return conn
    except (pyodbc.Error, TypeError) as e:
        print(f"Error connecting to database: {e}")
        raise


def execute_query(conn, query):
    """
    Execute a SQL query on the database connection.
    """
    try:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    except (pyodbc.Error, Exception) as e:
        print(f"Error executing query: {e}")
        raise


def getCustomers():
    """
    Example function to test the database connection.
    """
    query = """
        SELECT * FROM Customers;
    """
    return execute_query(connect_to_database(), query)


def main():
    print(getCustomers())


if __name__ == '__main__':
    main()