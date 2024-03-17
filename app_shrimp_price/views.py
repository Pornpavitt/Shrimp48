from django.shortcuts import render
from app_model.models import ShrimpPrices , User
import requests
from django.db.models import Avg
from django.http import JsonResponse
from datetime import datetime
# Create your views here.

# views.py

import requests
from django.shortcuts import render

def shrimpprice(request):
     # Get the selected date from the request parameters
    selected_date = request.GET.get('calendar')

    # Make sure selected_date is not None
    if selected_date:
        # Construct API URL with selected date
        api_url = f"https://dataapi.moc.go.th/gis-product-prices?product_id=P12004&from_date={selected_date}&to_date={selected_date}"
        
        # Make request to API
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
        else:
            data = {}
    else:
        # If selected_date is None, set data to an empty dictionary
        data = {}

    return render(request, 'app_shrimp_price/shrimp_price.html', {'data': data})

def shrimp_price_view(request):
    # Get current date and time
    current_date = datetime.now()

    # Pass current year, month, and day to the template context
    context = {
        'selected_year': current_date.year,
        'selected_month': current_date.month,
        'selected_day': current_date.day
    }

    return render(request, 'shrimp_price.html', context)
