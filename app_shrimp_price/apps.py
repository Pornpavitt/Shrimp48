from django.apps import AppConfig
from django.core.management import call_command


class MyAppConfig(AppConfig):
    name = 'api_commands'

    def ready(self):
        # Import your signal handlers here
        import api_commands.management.commands.fetch_shrimp_prices.sinal

        # Call the custom management command on server start
        call_command('fetch_shrimp_prices')

class AppShrimpPriceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_shrimp_price'
    # def ready(self):
    #     # Fetch API data when the server starts
    #     call_command('fetch_api_data')


    
