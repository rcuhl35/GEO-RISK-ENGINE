import itertools 
import pandas as pd

def buildCountryComparisons(alignedCountryData): 
    """
    Builds within-region country-level pairwise comparisons for BTL modeling
    
    Arguments:
        alignedCountryData: Trading-day-aligned dataset for each country
        
    Returns: 
        pd.DataFrame: Weekly within-region pairwise country comparisons
    """
    eventDayData = alignedCountryData[alignedCountryData['offset'] == 0].copy()

    if eventDayData['tradingDay'].dtype != 'datetime64[ns]':
        eventDayData['tradingDay'] = pd.to_datetime(eventDayData['tradingDay'])

    eventDayData['week'] = eventDayData['tradingDay'].dt.to_period('W')

    weeklyCountryTotals = eventDayData.groupby(['week', 'country'])['eventCount'].sum().reset_index()

    countryToRegion = eventDayData[['country', 'region']].drop_duplicates()
    weeklyCountryTotals = weeklyCountryTotals.merge(countryToRegion, on='country', how='left')

    comparisons = []

    for week, weekGroup in weeklyCountryTotals.groupby('week'):
        for region, regionGroup in weekGroup.groupby('region'): 
            countries = regionGroup['country'].tolist()
            counts = regionGroup.set_index('country')['eventCount']

            for countryI, countryJ in itertools.combinations(countries, 2):
                winsI = counts[countryI]
                total = counts[countryI] + counts[countryJ]

                comparisons.append({
                    'week' : week,
                    'region' : region, 
                    'countryI' : countryI, 
                    'countryJ' : countryJ, 
                    'winsI' : winsI, 
                    'total' : total
                })

    comparisons = pd.DataFrame(comparisons)
    comparisons = comparisons[comparisons['total'] > 0]

    return comparisons

    