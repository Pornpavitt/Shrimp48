import requests
from django.core.management.base import BaseCommand
from datetime import datetime
from app_model.models import ShrimpPrices

class Command(BaseCommand):
    help = 'Fetch data from the API and save it to the database'

    def handle(self, *args, **kwargs):
        # Define your API URL with the current date
        new_day = datetime.now().strftime('%Y-%m-%d')
        api_url = f"https://dataapi.moc.go.th/gis-product-prices?product_id=P12004&from_date={new_day}&to_date={new_day}"

        try:
            response = requests.get(api_url)
            data = response.json()

            if 'price_list' in data:
                for price_entry in data['price_list']:
                    date_str = price_entry['date']
                    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=None)
                    
                    # Check if an entry with the same date already exists
                    if not ShrimpPrices.objects.filter(date=date).exists():
                        ShrimpPrices.objects.create(
                            price_min=price_entry['price_min'],
                            price_max=price_entry['price_max'],
                            date=date
                        )
            else:
                self.stdout.write("No price list found in the API response.")
        except requests.exceptions.RequestException as e:
            self.stderr.write(f"API request error: {e}")
