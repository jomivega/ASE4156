import requests
from .models import Stock


def test_api_for_real_stock():
    ticker = "googl"
    name = "Google"
    url = "http://127.0.0.1:8000/stocks/addstock/"
    r = requests.post(url, data={'name': name, 'ticker': ticker})
    assert(r.status_code == 200)


def test_api_for_invalid_ticker():
    ticker = "xxx"
    name = "Julian"
    url = "http://127.0.0.1:8000/stocks/addstock/"
    r = requests.post(url, data={'name': name, 'ticker': ticker})
    assert(r.status_code == 500)


def test_api_for_existing_stock():
    ticker = "googl"
    name = "Google"
    url = "http://127.0.0.1:8000/stocks/addstock/"
    r = requests.post(url, data={'name': name, 'ticker': ticker})
    assert(r.status_code == 500)
    data = Stock.objects.all()
    print(data)


#test_api_for_real_stock()
test_api_for_existing_stock()
#test_api_for_invalid_ticker()
