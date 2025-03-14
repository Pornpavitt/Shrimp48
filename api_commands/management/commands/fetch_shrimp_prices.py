# myapp/management/commands/fetch_shrimp_prices.py
from django.core.management.base import BaseCommand
from app_model.models import ShrimpPrices
import requests
from datetime import datetime, timedelta
from pytz import timezone

class Command(BaseCommand):
    help = 'Fetch and store shrimp prices from API'

    def handle(self, *args, **kwargs):
        selected_date = datetime.now().strftime('%Y-%m-%d')
        api_url = f"https://dataapi.moc.go.th/gis-product-prices?product_id=P12004&from_date=2020-01-01&to_date={selected_date}"
        
        try:
            response = requests.get(api_url)
            data = response.json()
            if 'price_list' in data:
                for price_entry in data['price_list']:
                    date_str = price_entry['date']
                    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone('Asia/Bangkok'))
                    date += timedelta(days=1)
                    price_min = price_entry['price_min']
                    price_max = price_entry['price_max']
                    entry = ShrimpPrices.objects.filter(date=date).first()
                    if not entry:
                        ShrimpPrices.objects.create(
                            price_specie=data.get('product_name'), 
                            price_min=price_min,
                            price_max=price_max,
                            date=date,
                        )
        except requests.exceptions.RequestException as e:
            self.stderr.write(f"RequestException: {str(e)}")
        except ValueError as e:
            self.stderr.write(f"ValueError: Invalid JSON format in API response: {str(e)}")
