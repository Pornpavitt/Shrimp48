import requests
from django.shortcuts import render
from app_model.models import ShrimpPrices
from django.http import JsonResponse
from datetime import datetime, timedelta
from pytz import timezone

def shrimpprice(request):
    selected_date = request.GET.get('calendar')

    if selected_date:
        api_url = f"https://dataapi.moc.go.th/gis-product-prices?product_id=P12004&from_date={selected_date}&to_date={selected_date}"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for 4XX or 5XX status codes
            data = response.json()
            if 'price_list' in data:
                for price_entry in data['price_list']:
                    # Extracting relevant information from the API response
                    date_str = price_entry['date']
                    # Parse the date string and add one day to it
                    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone('Asia/Bangkok'))
                    date += timedelta(days=1)  # Add one day
                    # Format the date as string in the specified format
                    formatted_date_str = date.strftime('%Y-%m-%d %H:%M:%S')
                    price_min = price_entry['price_min']
                    price_max = price_entry['price_max']

                    # Check if the entry already exists in the database
                    existing_entry = ShrimpPrices.objects.filter(date=date).first()
                    if not existing_entry:
                        # If the entry doesn't exist, create and save it
                        shrimp_price = ShrimpPrices.objects.create(
                            price_specie=data.get('product_name', ''),  # Assuming 'product_name' as price_specie
                            price_min=price_min,
                            price_max=price_max,
                            date=date,  # Assigning the localized datetime
                        )
                        shrimp_price.save()
        except requests.exceptions.RequestException as e:
            # Handle request exceptions
            return JsonResponse({'error': str(e)}, status=500)
        except ValueError as e:
            # Handle JSON decoding error
            return JsonResponse({'error': 'Invalid JSON format in API response'}, status=500)
    else:
        data = None

    return render(request, 'app_shrimp_price/shrimp_price.html', {'data': data})
