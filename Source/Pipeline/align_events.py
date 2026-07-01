import pandas as pd

def matchToTradingDay(eventDate, tradingDays): 
    """
    Match an event date to the nearest trading day.
    
    Arguments:
        eventDate: The date of the event.
    tradingDays: The index of valid trading days.
    
    Returns:
        The nearest trading day 
    
    """
    index = tradingDays.searchsorted(eventDate)
    index = min(index, len(tradingDays) - 1)
    return tradingDays[index]

def getEventWindow(tradingDay, marketReturns, before=1, after=3):
    """
    Extract returns for a [-before, +after] window around a given trading day.

    Arguments:
        tradingDay: The trading day around which to extract returns.
        marketReturns: A DataFrame of market returns indexed by trading day.
        before: Number of days before the trading day to include.
        after: Number of days after the trading day to include.

    Returns: 
        A DataFrame of returns for the specified window (or None if out of range)
    """

    index = marketReturns.index.searchsorted(tradingDay)
    startIndex = index - before
    endIndex = index + after + 1

    if startIndex < 0 or endIndex > len(marketReturns):
        return None
    
    eventWindow = marketReturns.iloc[startIndex:endIndex].copy()
    eventWindow['offset'] = range(-before, after + 1)

    return eventWindow 
