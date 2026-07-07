import itertools 
import pandas as pd

def buildComparisons(alignedData): 
    """
    Builds a comparison dataframe from the aligned data for BTL modeling 
    
    Arguments:
        alignedData (pd.DataFrame): Data frame containing tradingDay, region event counts, and returns
    
    Returns: 
        pd.DataFrame: A dataframe containing all possible comparisons of event types for each date.
    """
    if alignedData['tradingDay'].dtype != 'datetime64[ns]':
        alignedData['tradingDay'] = pd.to_datetime(alignedData['tradingDay'])

    alignedData['week'] = alignedData['tradingDay'].dt.to_period('W')

    regions = ['events_CaucasusCA', 'events_Europe', 'events_MiddleEast', 'events_NorthAfrica']

    weeklyTotals = alignedData.groupby('week')[regions].sum() 

    comparisons = []

    for week, row in weeklyTotals.iterrows():
        for regionI, regionJ in itertools.combinations(regions, 2):
            winsI = row[regionI]
            total = row[regionI] + row[regionJ]

            comparisons.append({
                'week' : week,
                'regionI' : regionI.replace('events_', ''),
                'regionJ' : regionJ.replace('events_', ''),
                'winsI' : winsI,
                'total' : total
            })

    comparisons = pd.DataFrame(comparisons)
    comparisons = comparisons[comparisons['total'] > 0]

    return comparisons
    

