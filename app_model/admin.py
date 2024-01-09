from django.contrib import admin
from .models import ShrimpSpecies, ShrimpFoods, ShrimpDiseases, ShrimpPrices, ShrimpPonds, ShrimpPondsDetail

# Register your models here.

@admin.register(ShrimpSpecies)
class ShrimpSpeciesAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']

@admin.register(ShrimpFoods)
class ShrimpFoodsAdmin(admin.ModelAdmin):
    list_display = ['food_Name', 'food_description', 'created_at']
    search_fields = ['food_Name']

@admin.register(ShrimpDiseases)
class ShrimpDiseasesAdmin(admin.ModelAdmin):
    list_display = ['disease_Name', 'disease_Symptom', 'created_at']
    search_fields = ['disease_Name']

@admin.register(ShrimpPrices)
class ShrimpPricesAdmin(admin.ModelAdmin):
    list_display = ['price', 'created_at']
    search_fields = ['price']

@admin.register(ShrimpPonds)
class ShrimpPondsAdmin(admin.ModelAdmin):
    list_display = ['UserID', 'pond_number', 'created_at']
    search_fields = ['pond_number']

@admin.register(ShrimpPondsDetail)
class ShrimpPondsDetailAdmin(admin.ModelAdmin):
    list_display = ['pondID', 'shrimp_Quantity', 'created_at']
    search_fields = ['pondID__pond_number']
