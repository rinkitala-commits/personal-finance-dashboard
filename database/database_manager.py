import sqlite3


DATABASE_NAME = "database/finance.db"


def create_connection():
    """
    Create a connection to the SQLite database.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    return connection

def create_transactions_table():
    """
    Create the transactions table if it doesn't exist.
    """

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            date TEXT NOT NULL,

            category TEXT NOT NULL,

            description TEXT,

            amount REAL NOT NULL,

            type TEXT NOT NULL

        )
    """)

    connection.commit()
    connection.close()

