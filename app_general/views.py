from django.shortcuts import render
from django.http.response import HttpResponse
from app_model.models import ShrimpDiseases,ShrimpFoods,ShrimpSpecies,ShrimpPrices
from django.db.models import Max

# Create your views here.
def home(request):
    species = ShrimpSpecies.objects.filter(deleted_at = None)
    food = ShrimpFoods.objects.filter(deleted_at = None)
    disease = ShrimpDiseases.objects.filter(deleted_at = None)
    # Find the latest date
    latest_date = ShrimpPrices.objects.filter(deleted_at=None).aggregate(latest_date=Max('date'))['latest_date']
    
    # Filter the shrimp prices by the latest date
    shrimpprice = ShrimpPrices.objects.filter(deleted_at=None, date=latest_date)

    context = {'species':species, 'food':food, 'disease':disease, 'shrimpprice' :shrimpprice}
    return render(request, 'app_general/home.html',context)

def howtouse(request):
    return render(request, 'app_general/howtouse.html')

def shrimp_diseases(request):
    disease = ShrimpDiseases.objects.filter(deleted_at = None)
    return render(request, 'app_general/shrimp_diseases.html',{'disease':disease})

def shrimp_food(request):
    food = ShrimpFoods.objects.filter(deleted_at = None)
    return render(request,'app_general/shrimp_food.html',{'food':food})

def shrimp_species(request):
    species = ShrimpSpecies.objects.filter(deleted_at = None)
    return render(request,'app_general/shrimp_species.html',{'species':species})

def hometest(request):
    species = ShrimpSpecies.objects.filter(deleted_at = None)
    food = ShrimpFoods.objects.filter(deleted_at = None)
    disease = ShrimpDiseases.objects.filter(deleted_at = None)
    context = {'species':species, 'food':food, 'disease':disease}
    return render(request, 'app_general/hometest.html',context)