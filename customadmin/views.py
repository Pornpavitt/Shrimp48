from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from app_model.models import ShrimpSpecies, ShrimpFoods, ShrimpDiseases, ShrimpPrices, ShrimpPonds, ShrimpPondsDetail
from django.urls import reverse
# Create your views here.

def admin(request):
    if request.User.is_superuser:
        return render(request, 'customadmin/dashboard.html')
    else:
        return  HttpResponse("You are not authorized to access this page.")
    
def admin_login(request,):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password )
        if user is not None:
            login(request, user)
            return redirect("dashboard/")  # Corrected the redirect URL
        else:
            return render(request, 'customadmin/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'customadmin/login.html')
    
def dashboard(request):
    if request.user.is_superuser:
        users = User.objects.all()
        shrimp_species = ShrimpSpecies.objects.all()
        shrimp_species = ShrimpSpecies.objects.all()
        shrimp_foods = ShrimpFoods.objects.all()
        shrimp_diseases = ShrimpDiseases.objects.all()
        shrimp_prices = ShrimpPrices.objects.all()
        shrimp_ponds = ShrimpPonds.objects.all()
        shrimp_ponds_detail = ShrimpPondsDetail.objects.all()

        return render(request, 'customadmin/dashboard.html', {
            'users' : users,
            'shrimp_species': shrimp_species,
            'shrimp_foods': shrimp_foods,
            'shrimp_diseases': shrimp_diseases,
            'shrimp_prices': shrimp_prices,
            'shrimp_ponds': shrimp_ponds,
            'shrimp_ponds_detail': shrimp_ponds_detail,
    })

    else:
        return  render(request,"customadmin/login.html")
    
#######
#User##
#######
def user(request):
    users = User.objects.all()
    return render(request, 'customadmin/user.html', {'users' : users})

def add_users(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_superuser = request.POST.get('is_superuser')

        # Create a new user object
        new_user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_superuser=is_superuser,
            is_staff=False, 
            is_active=True
        )
        return redirect('add_users')
    
    elif request.method == 'GET':
        return render(request, 'customadmin/add_users.html') 
    
def edit_user(request, user_id):
    if request.method == 'POST':
        users = User.objects.get(id=user_id)
        users.first_name = request.POST['first_name']
        users.last_name = request.POST['last_name']
        users.save()
        return redirect('user')
    else:
        users = User.objects.get(id=user_id)
        return render(request, 'customadmin/edit_user.html', {"users": users})

def delete_user(request, user_id):
    users = User.objects.get(id=user_id)
    users.is_active = False
    users.save()
    return redirect('user')   

    
def create_shrimp_species(request):
    if request.method == 'POST':
        # Retrieve the user object based on the user ID
        user_id = request.POST['UserID']
        user = User.objects.get(id=user_id)
        # Create a new instance of ShrimpSpecies
        new_instance = ShrimpSpecies(UserID=user, name=request.POST['name'])
        new_instance.save()
        return redirect('dashboard')
    return render(request, 'customadmin/add_shrimp_species.html')

