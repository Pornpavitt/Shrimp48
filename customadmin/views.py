from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from app_model.models import ShrimpSpecies, ShrimpFoods, ShrimpDiseases, ShrimpPrices, ShrimpPonds, ShrimpPondsDetail
import datetime
from django import forms
# Create your views here.

def admin(request):
    if request.User.is_superuser:
        return render(request, 'customadmin/dashboard.html')
    else:
        return  HttpResponse("You are not authorized to access this page.")

@staff_member_required
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

@staff_member_required
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
@staff_member_required
def user(request):
    users = User.objects.all()
    return render(request, 'customadmin/user.html', {'users' : users})

@staff_member_required
def add_users(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_superuser = request.POST.get('is_superuser')
        image = request.FILES.get('image')
        # Create a new user object
        new_user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_superuser=is_superuser,
            image=image,
            is_staff=False, 
            is_active=True
        )
        return redirect('user')
    
    elif request.method == 'GET':
        return render(request, 'customadmin/add_users.html') 
    
@staff_member_required   
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

@staff_member_required
def delete_user(request, user_id):
    users = User.objects.get(id=user_id)
    users.is_active = False
    users.save()
    return redirect('user')   



############################
####shrimpSpecies Admin#####
############################
@staff_member_required
def shrimpSpecies(request):
    species = ShrimpSpecies.objects.filter(deleted_at=None)
    return render(request, 'customadmin/shrimpSpecies.html', {'species' : species})

@staff_member_required
def add_shrimpSpecies(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        specie_food = request.POST.get('specie_food')
        image = request.FILES.get('image')
        user_id = request.POST.get('userid')
        print(request.FILES)
        # Create a new user object
        new_species = ShrimpSpecies.objects.create(
            name=name,
            description=description,
            specie_food=specie_food,
            image=image,
            user_id=user_id
        )
        return redirect('shrimpSpecies')
    elif request.method == 'GET':
        return render(request, 'customadmin/add_shrimpSpecies.html') 

@staff_member_required
def edit_species(request, specie_id):
    if request.method == 'POST':
        species = ShrimpSpecies.objects.get(id=specie_id)
        species.name = request.POST['name']
        species.description = request.POST['description']
        species.specie_food = request.POST['specie_food']
        species.image = request.FILES['image']
        user_id = request.POST.get('userid')
        species.save()
        return redirect('shrimpSpecies')
    else:
        species = ShrimpSpecies.objects.get(id=specie_id)
        return render(request, 'customadmin/edit_shrimpSpecies.html', {"species": species})

@staff_member_required
def delete_species(request, specie_id):
    species = ShrimpSpecies.objects.get(id=specie_id)
    species.deleted_at = datetime.datetime.now()
    species.save()
    return redirect('shrimpSpecies')   

###################
####shrimpFood#####
###################
@staff_member_required
def shrimpFoods(request):
    foods = ShrimpFoods.objects.filter(deleted_at=None)
    return render(request, 'customadmin/shrimpFoods.html', {'foods' : foods})

@staff_member_required
def add_shrimpFoods(request):
    if request.method == 'POST':
        food_name = request.POST.get('food_name')
        food_description = request.POST.get('food_description')
        food_image = request.FILES.get('food_image')
        user_id = request.POST.get('userid')

        # Create a new user object
        new_foods = ShrimpFoods.objects.create(
            food_name=food_name,
            food_description=food_description,
            food_image=food_image,
            user_id=user_id
        )
        return redirect('shrimpFoods')
    elif request.method == 'GET':
        return render(request, 'customadmin/add_shrimpfood.html') 

@staff_member_required
def edit_shrimpFoods(request, food_id):
    if request.method == 'POST':
        foods = ShrimpFoods.objects.get(id=food_id)
        foods.food_name = request.POST['food_name']
        foods.food_description = request.POST['food_description']
        foods.food_image = request.FILES['food_image']
        user_id = request.POST.get('userid')
        foods.save()
        return redirect('shrimpFoods')
    else:
        foods = ShrimpFoods.objects.get(id=food_id)
        return render(request, 'customadmin/edit_shrimpFoods.html', {"foods": foods})

@staff_member_required
def delete_shrimpFoods(request, food_id):
    species = ShrimpFoods.objects.get(id=food_id)
    species.deleted_at = datetime.datetime.now()
    species.save()
    return redirect('shrimpFoods')   

###################
####shrimpDiseases#####
###################
@staff_member_required
def shrimpDiseases(request):
    diseases = ShrimpDiseases.objects.filter(deleted_at=None)
    return render(request, 'customadmin/shrimpDiseases.html', {'diseases' : diseases})

@staff_member_required
def add_shrimpDiseases(request):
    if request.method == 'POST':
        disease_name = request.POST.get('disease_name')
        disease_symptom = request.POST.get('disease_symptom')
        disease_image = request.FILES.get('disease_image')
        disease_prevent = request.POST.get('disease_prevent')
        disease_treat = request.POST.get('disease_treat')
        disease_cause =  request.POST.get('disease_cause')
        user_id = request.POST.get('userid')

        # Create a new user object
        new_diseases = ShrimpDiseases.objects.create(
            disease_name=disease_name,
            disease_symptom=disease_symptom,
            disease_image=disease_image,
            disease_prevent=disease_prevent,
            disease_treat=disease_treat,
            disease_cause=disease_cause,
            user_id=user_id
        )
        return redirect('shrimpDiseases')
    
    elif request.method == 'GET':
        return render(request, 'customadmin/add_shrimpdiseases.html') 

@staff_member_required
def edit_shrimp_diseases(request, disease_id):
    if request.method == 'POST':
        disease = ShrimpDiseases.objects.get(id=disease_id)
        disease.disease_name = request.POST.get('disease_name')
        disease.disease_symptom = request.POST.get('disease_symptom')
        disease.disease_image = request.FILES.get('disease_image')
        disease.disease_prevent = request.POST.get('disease_prevent')
        disease.disease_treat = request.POST.get('disease_treat')
        disease.disease_cause = request.POST.get('disease_cause')
        user_id = request.POST.get('userid')
        disease.user_id = user_id
        disease.save()
        return redirect('shrimpDiseases')
    else:
        disease = ShrimpDiseases.objects.get(id=disease_id)
        return render(request, 'customadmin/edit_shrimpDiseases.html', {"disease": disease})


@staff_member_required
def delete_shrimp_diseases(request, disease_id):
    disease = ShrimpDiseases.objects.get(id=disease_id)
    disease.deleted_at = datetime.datetime.now()
    disease.save()
    return redirect('shrimpDiseases')