from django.contrib import admin
from .models import ShrimpSpecies, ShrimpFoods, ShrimpDiseases, ShrimpPrices, ShrimpPonds, ShrimpPondsDetail

admin.site.register([ShrimpSpecies, ShrimpFoods, ShrimpDiseases, ShrimpPrices, ShrimpPonds, ShrimpPondsDetail])
