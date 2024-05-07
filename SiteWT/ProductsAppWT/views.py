from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product
from .models import Historical
from .service import get_fetched_data,get_Products_added,get_Product_detail,update_Product,add_Product,delete_Product
#import response
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


# Create your views here.

def index(request):
    products=get_Products_added()
    context={
        'products':products
        }
    return render(request,'ProductsAppWT/index.html',context)
    

def products(request):
    return HttpResponse("Test")

def product_detail(request,id):
    product= get_Product_detail(id)
    context={
        'product':product
        }
    return render(request,'ProductsAppWT/detail.html',context)

def product_add(request):
    if request.method=='POST':
        name=request.POST.get('name')
        ticker=request.POST.get('ticker')
        add_Product(name,ticker)
        return redirect('/products/')
    return render(request, 'ProductsAppWT/add.html')

def product_update(request,id):
    product= get_Product_detail(id)
    if request.method=='POST':
        name=request.POST.get('name')
        ticker=request.POST.get('ticker')
        update_Product(name,ticker)
        return redirect('/products/')

    context={
        'product':product
        }
    return render(request, 'ProductsAppWT/update.html', context)


def product_delete(request,id):
    product= get_Product_detail(id)
    if request.method=='POST':
        delete_Product(id)
        return redirect('/products/')

    context={
        'product':product
        }
    return render(request, 'ProductsAppWT/delete.html', context)


def coinbase_data(request):
    end_date = datetime.now()
    ret_ser=get_fetched_data()
    return HttpResponse(json.dumps(ret_ser))

def get_json_response(url):
    """Utility function to send GET request and return JSON response."""
    try:
        response = session.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except requests.RequestException:
        #print(f"Request failed: {e}")
        return None


def process_data(products):
    """Utility function to process data"""
    df=pd.DataFrame(products, columns=["time", "low","high","open","close","volume"]) 
    df["date"]=pd.to_datetime(df["time"], unit='s')
    print(df)

def historical_data(request):
     historical= Historical.objects.all()
     for hist in historical:
        print(hist.timestamp)
     context={
        'historical':historical
        }
     return render(request,'ProductsAppWT/historialDetails.html',context)
