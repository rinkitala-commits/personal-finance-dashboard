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

import pandas as pd


def import_csv_to_database(csv_file):
    """
    Import transactions from CSV into SQLite.
    """

    df = pd.read_csv(csv_file)

    connection = create_connection()

    df.to_sql(
        "transactions",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

def view_transactions():
    """
    Display all transactions from SQLite.
    """

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transactions")

    rows = cursor.fetchall()

    connection.close()

    return rows

def load_transactions_from_database():
    """
    Load transactions from the SQLite database.
    """

    connection = create_connection()

    query = """
    SELECT
        rowid AS transaction_id,
        date AS Date,
        description AS Description,
        amount AS Amount,
        category AS Category
    FROM transactions
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Create Income and Expense columns
    # based on the existing Amount values.
    #
    # Positive Amount = Income
    # Negative Amount = Expense

    df["Income"] = df["Amount"].where(
        df["Amount"] > 0,
        0
    )

    df["Expense"] = df["Amount"].where(
        df["Amount"] < 0,
        0
    ).abs()

    return df

def show_table_structure():
    """
    Show the columns of the transactions table.
    """

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(transactions)")

    columns = cursor.fetchall()

    connection.close()

    return columns

def add_transaction(date, description, amount, category):
    """
    Add a new transaction to the SQLite database.
    """

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO transactions
        (Date, Description, Amount, Category)
        VALUES (?, ?, ?, ?)
        """,
        (date, description, amount, category)
    )

    connection.commit()
    connection.close()

def delete_transaction(transaction_id):
    """
    Delete a transaction from the SQLite database using its ID.
    """

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM transactions
        WHERE rowid = ?
        """,
        (transaction_id,)
    )

    connection.commit()
    connection.close()

def delete_transaction(transaction_id):
    """
    Delete one transaction from the SQLite database.
    """

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM transactions
        WHERE rowid = ?
        """,
        (transaction_id,)
    )

    connection.commit()
    connection.close()