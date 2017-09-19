"""This module is for loading historical data for stocks"""
from yahoo_historical import Fetcher

import arrow
from .models import Stock, DailyStockQuote


def data_ten_years_back_for_stock(request):
    """ Function that creates Stock object
        and loads data for it 10 years back
    """
    if request.method == "POST":
        body = request.POST
        name = body['name']
        ticker = body['ticker']
        stock = Stock(name=name, ticker=ticker)
        stock.save()
        now = arrow.now()
        ten_back = now.replace(years=-10)
        now = get_date_array_for_fetcher(now)
        ten_back = get_date_array_for_fetcher(ten_back)
        fetcher = Fetcher(ticker, ten_back, now)
        history = fetcher.getHistorical()
        objects = []
        for row in history.itertuples():
            value = getattr(row, "Close")
            date = getattr(row, "Date")
            objects.append(
                DailyStockQuote(value=value, date=date, stock=stock))
        DailyStockQuote.objects.bulk_create(objects, batch_size=500)


def get_date_array_for_fetcher(arrow_date):
    """Function that formats arrow date to Yahoo Fetcher format """
    return [arrow_date.year, arrow_date.month, arrow_date.day]
