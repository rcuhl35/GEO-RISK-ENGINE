import pandas as pd

def cleanACLED(filepath):
    """
    Loads and cleans the ACLED dataset from a CSV file.
    
    Arguments:
        filepath (str): The path to the ACLED CSV file.
    
    Returns: 
        cleaned ACLED data with event_date converted to datetime
    """ 
    data = pd.read_csv(filepath, low_memory=False)
    data['event_date'] = pd.to_datetime(data['event_date'])
    return data