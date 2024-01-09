from django.contrib import admin
from .models import ShrimpSpecies
# Register your models here.

class ShrimpSpeciesAdmin(admin.ModelAdmin):
    list_display = ['name','food','description','created_at']
    search_fields = ['name']
    list_filter = ['food']

admin.site.register(ShrimpSpecies, ShrimpSpeciesAdmin)