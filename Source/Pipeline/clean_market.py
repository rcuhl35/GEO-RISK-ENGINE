import pandas as pd

def cleanMarket(filepath):
    """
    Loads and cleans the Market dataset from a CSV file.
    
    Arguments:
        filepath (str): The path to the Market CSV file.

    Returns: 
        Cleaned Market data with date parsed as datetime index
    """
    data = pd.read_csv(filepath, index_col='Date', parse_dates=True)
    return data