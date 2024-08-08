from django.test import TestCase
# yourapp/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . models import *
import requests

def home(request):
   return render(request,'Home.html')

def stockreg(request):
    global global_symbol
    if request.method=='POST':
        symbol=request.POST.get('symbol')
        price=request.POST.get('price')
        log=sdetails(symbol=symbol,price=price)
        log.save()
        return redirect(stockreg)
    return render(request,'Home.html')

global_symbol = sdetails.objects.last()

class StockFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36'
        }
        self.session = requests.Session()
        self.session.get("https://www.nseindia.com", headers=self.headers)

    def stockfetch(self, symbol):
        if not symbol:
            return None  # Handle case where symbol is None
        url = f'https://www.nseindia.com/api/chart-databyindex?index={symbol}'
        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

def fetch_latest_stock_data():
    global_symbol = sdetails.objects.last()
    if global_symbol and global_symbol.symbol:
        stock_fetcher = StockFetcher()
        stock_data = stock_fetcher.stockfetch(global_symbol.symbol)
        return stock_data
    return None

# Example usage:
stock_data = fetch_latest_stock_data()
if stock_data:
    print(stock_data)
else:
    print("Failed to fetch stock data")


