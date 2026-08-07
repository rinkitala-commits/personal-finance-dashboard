import pandas as pd

DATA_FILE = "data/transactions.csv"


def load_transactions():
    """
    Load transactions from CSV.
    """
    return pd.read_csv(DATA_FILE)


def save_transactions(df):
    """
    Save transactions to CSV.
    """
    df.to_csv(DATA_FILE, index=False)