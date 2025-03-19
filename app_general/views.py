from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseRedirect
from app_model.models import ShrimpDiseases,ShrimpFoods,ShrimpSpecies,ShrimpPrices,User
from django.db.models import Max
from app_users.forms import RegisterForm
from django.urls import reverse
from django.contrib.auth import login
# Create your views here.
def home(request):
    species = ShrimpSpecies.objects.filter(allow_show = 1,deleted_at = None)
    food = ShrimpFoods.objects.filter(allow_show = 1,deleted_at = None)
    disease = ShrimpDiseases.objects.filter(allow_show = 1,deleted_at = None)
    latest_date = ShrimpPrices.objects.filter(
        deleted_at=None, 
        price_specie="กุ้งขาว (70 ตัว/กก.)" 
    ).aggregate(latest_date=Max('date'))['latest_date']
    shrimpprice = ShrimpPrices.objects.filter(deleted_at=None, date=latest_date)

    user = request.user if request.user.is_authenticated else None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request ,user)
            return HttpResponseRedirect(reverse("home"))
    else:
        form = RegisterForm()
    context = {'species':species, 'food':food, 'disease':disease, 'shrimpprice' :shrimpprice,'user':user,'form' : form}
    
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