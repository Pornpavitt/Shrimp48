from django.shortcuts import render
from django.http.response import HttpResponse
from app_model.models import ShrimpDiseases,ShrimpFoods,ShrimpSpecies

# Create your views here.
def home(request):
    return render(request, 'app_general/home.html')

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