from django.shortcuts import render
from app_model.models import ShrimpPrices , User
import requests
from django.db.models import Avg
from django.http import JsonResponse
import datetime
# Create your views here.

# views.py

import requests
from django.shortcuts import render

def shrimpprice(request):
    api_url = "https://dataapi.moc.go.th/gis-product-prices?product_id=P12004&from_date=2024-01-01&to_date=2025-11-11"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
    else:
        data = {}
    return render(request, 'app_shrimp_price/shrimp_price.html', {'data':data})
        
