"""This module is for loading historical data for stocks"""
from yahoo_historical import Fetcher

import arrow
from .models import Stock, DailyStockQuote

def loadData10YearsBackFromTodayForStock(request):
    """Function that creates Stock object and loads data for it 10 years back"""
    if request.method == "POST":
        body = request.POST
        name = body['name']
        ticker = body['ticker']
        stock = Stock(name=name, ticker=ticker)
        stock.save()
        now = arrow.now()
        tenBack = now.replace(years=-10)
        now = getDateArrayForFetcher(now)
        tenBack = getDateArrayForFetcher(tenBack)
        fetcher = Fetcher(ticker, tenBack, now)
        history = fetcher.getHistorical()
        for row in history.itertuples():
            value = getattr(row, "Close")
            date = getattr(row, "Date")
            DailyStockQuote(value=value, date=date, stock=stock).save()

def getDateArrayForFetcher(arrowDate):
    """Function that formats arrow date to Yahoo Fetcher format """
    return [arrowDate.year, arrowDate.month, arrowDate.day]
