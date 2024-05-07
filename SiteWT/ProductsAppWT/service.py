from django.db import models
from .models import Product
from .models import Historical
import json
import requests
import http
from django.http import JsonResponse
import time
from datetime import datetime, timedelta
import pandas as pd

# Create a session for HTTP requests
session = requests.Session()
session.headers.update({
    'Content-Type': 'application/json',
    'User-Agent': 'Python http.client'
})


def get_Products_added():
     return Product.objects.all()

def get_Product_detail(id):
     return Product.objects.get(id=id)

def add_Product(name,ticker):
     product=Product(name=name,ticker=ticker)
     product.save()

def update_Product(name,ticker):
     product.name=request.POST.get('name')
     product.ticker=request.POST.get('ticker')
     product.save()

def delete_Product(id):
     product= Product.objects.get(id=id)
     product.delete()
     

def get_fetched_data():
     products_added=get_Products_added()
     end_date = datetime.now()
     start_date = end_date - timedelta(minutes=2)
     print(end_date)
     print(start_date)
     for product in products_added:
         tickername= product.ticker
         url= get_url(tickername,start_date,end_date)
         print(url)
         historical_data = get_json_response(url)
         insert_historical_data(historical_data,product.id)
    
     return historical_data



def get_url(token,start_date,end_date):
    return f'https://api.pro.coinbase.com/products/{token}/candles?start={start_date.strftime("%Y-%m-%d")}&end={end_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z")}&granularity=21600'


def get_json_response(url):
    """Utility function to send GET request and return JSON response."""
    try:
        response = session.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except requests.RequestException:
        #print(f"Request failed: {e}")
        return None

def insert_historical_data(historical_data,id):
    """Utility function to send GET request and return JSON response."""
    try:
        cur_data = Historical.objects.filter(ticker_id=id)
        max_date = cur_data.latest('timestamp')
        print(max_date.timestamp)
        df=pd.DataFrame(historical_data, columns=["time", "low","high","open","close","volume"]) 
        df["date"]=pd.to_datetime(df["time"], unit='s')
        print(df)
        for index, row in df.iterrows():
            if row['date'] > max_date.timestamp:
                obj = Historical(
                    ticker_id=id,
                    #timestamp=datetime.strptime(row['date'], "%Y-%m-%dT%H:%M:%S.%f%z").date(),
                    timestamp=row['date'],
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close']
                 )
                obj.save()
        
        fet= Historical.objects.count()
        print(fet)


    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None