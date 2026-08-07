import pandas as pd


def to_csv(dataframe):
    """
    Convert a DataFrame to CSV.
    """
    return dataframe.to_csv(index=True)