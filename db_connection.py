import mysql.connector as con
import os

def get_database_connection():
    """
    Establish and return a connection to the MySQL database.
    Returns:
        connection (MySQLConnection): A MySQL database connection object.
    """
    try:
        connection = con.connect(
            host="localhost",
            user="root",
            passwd="Kio23gamer!?...",
            database="canteen_automation"
        )
        return connection
    except con.Error as e:
        print(f"\nError connecting to database: {e}")
        return None

def get_cursor(connection):
    """
    Provides a cursor object for database operations.
    Args:
        connection (MySQLConnection): A MySQL database connection object.
    Returns:
        cursor (MySQLCursor): Cursor object for database operations.
    """
    if connection:
        return connection.cursor(buffered=True)
    else:
        return None

def close_connection(cursor, connection):
    """
    Closes the database cursor and connection.
    """
    if cursor:
        cursor.close()
    if connection:
        connection.close()
