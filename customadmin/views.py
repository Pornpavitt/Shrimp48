from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from app_model.models import ShrimpSpecies, ShrimpFoods, ShrimpDiseases, ShrimpPrices, ShrimpPonds, ShrimpPondsDetail, Information,water_quality
from datetime import datetime, timedelta
from django import forms
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from django.db.models import Max
from pytz import timezone
from django.utils.timezone import make_aware

# Create your views here.
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error

def admin(request):
    if request.User.is_superuser:
        return render(request, 'customadmin/dashboard.html')
    else:
        return  HttpResponse("You are not authorized to access this page.")

def predict_price(request):
    if request.method == 'POST':
        months_ahead = int(request.POST.get('months_ahead', 1))  
        yearY = int(request.POST.get('yearY')) 
        monthY = int(request.POST.get('monthY'))

        predicted_price = predict(yearY, monthY, months_ahead)
        

    return redirect('dashboard')

def predict(yearY,monthY, months_ahead=1):
    shrimpprice = ShrimpPrices.objects.values('date','price_min','price_max')
    df = pd.DataFrame(shrimpprice)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df['price_min'] = df['price_min'].astype(float)
    df['price_max'] = df['price_max'].astype(float)
    print(df.head())  
    print(df.dtypes)  

    df[["year","month","day"]] = df.date.str.split("-", expand=True)
    df['average'] = df['price_min']+df['price_max']
    df['average'] = df['average']/2
    df_dropped = df.drop(columns=['price_min', 'price_max'], axis=1)

    df_select = df_dropped
    df_select['date'] = pd.to_datetime(df_select['date'])

    df_select=df_select[(df_select['date'].dt.year==yearY)]

    dp = pd.pivot_table(df_select, index=["month"],values=["average"],aggfunc=np.average)

    x = dp.index.values.reshape(-1,1)
    dfpoly = PolynomialFeatures(degree=2)
    x_poly = dfpoly.fit_transform(x)
    y = dp.average
    model = LinearRegression()
    model.fit(x_poly,y)

    future_month = monthY + months_ahead
    y_predict_Future = model.predict(dfpoly.fit_transform([[future_month]]))
    
    
    future_date = datetime(yearY, future_month, 28) 

    ShrimpPrices.objects.create(
        date=future_date,
        price_specie="Predicted",  
        price_min=None,  
        price_max=None,  
        predict=y_predict_Future[0]
    )
    return y_predict_Future[0]

def update_price(request):
    if request.method == 'POST' and request.POST.get('submit'):
        api_url = "https://dataapi.moc.go.th/gis-product-prices?product_id=P12004&from_date=2020-01-01&to_date=2025-12-31"

        try:
            response = requests.get(api_url, verify=False)  
            response.raise_for_status()  
            try:
                data = response.json()  
            except ValueError as e:
                return JsonResponse({'error': 'Invalid JSON format in API response', 'details': str(e)}, status=500)

            if 'price_list' in data:
                for price_entry in data['price_list']:
                    date_str = price_entry.get('date')
                    if date_str:
                        date = make_aware(datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S'), timezone('Asia/Bangkok'))
                        price_min = price_entry.get('price_min')
                        price_max = price_entry.get('price_max')

                        ShrimpPrices.objects.get_or_create(
                            date=date,
                            defaults={
                                'price_specie': data.get('product_name'),
                                'price_min': price_min,
                                'price_max': price_max
                            }
                        )

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'No date selected'}, status=400)
    
    return redirect('dashboard')



@staff_member_required
def dashboard(request):
    if request.user.is_superuser:
        users = User.objects.all()
        shrimp_species = ShrimpSpecies.objects.filter(deleted_at = None)
        shrimp_species = ShrimpSpecies.objects.filter(deleted_at = None)
        shrimp_foods = ShrimpFoods.objects.filter(deleted_at = None)
        shrimp_diseases = ShrimpDiseases.objects.filter(deleted_at = None)
        shrimp_ponds = ShrimpPonds.objects.filter(deleted_at = None)
        shrimp_ponds_detail = ShrimpPondsDetail.objects.filter(deleted_at = None)
        information = Information.objects.filter(deleted_at = None)
        latest_date = ShrimpPrices.objects.filter(
            deleted_at=None, 
            price_specie="กุ้งขาว (70 ตัว/กก.)" 
        ).aggregate(latest_date=Max('date'))['latest_date']
        shrimp_prices = ShrimpPrices.objects.filter(deleted_at=None, date=latest_date)
        latest_date_predict = ShrimpPrices.objects.filter(
            deleted_at=None, 
            price_specie="Predicted" 
        ).aggregate(latest_date=Max('date'))['latest_date']
        pre_price = ShrimpPrices.objects.filter(deleted_at=None, date=latest_date_predict)
        print('f',pre_price)


        return render(request, 'customadmin/dashboard.html', {
            'users' : users,
            'shrimp_species': shrimp_species,
            'shrimp_foods': shrimp_foods,
            'shrimp_diseases': shrimp_diseases,
            'shrimp_prices': shrimp_prices,
            'shrimp_ponds': shrimp_ponds,
            'shrimp_ponds_detail': shrimp_ponds_detail,
            'information': information,
            'pre_price':pre_price
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
        if 'image' in request.FILES:
            users.image = request.FILES['image']
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
        allow_show = request.POST.get('allow_show')
        user_id = request.POST.get('userid')
        # print(request.FILES)
        # Create a new user object
        new_species = ShrimpSpecies.objects.create(
            name=name,
            description=description,
            specie_food=specie_food,
            image=image,
            allow_show = allow_show,
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
        if 'image' in request.FILES:
            species.image = request.FILES['image']
        species.allow_show = request.POST.get('allow_show')
        user_id = request.POST.get('userid')
        species.save()
        return redirect('shrimpSpecies')
    else:
        species = ShrimpSpecies.objects.get(id=specie_id)
        return render(request, 'customadmin/edit_shrimpSpecies.html', {"species": species})

@staff_member_required
def delete_species(request, specie_id):
    species = ShrimpSpecies.objects.get(id=specie_id)
    species.deleted_at = datetime.now()
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
        allow_show = request.POST.get('allow_show')
        user_id = request.POST.get('userid')

        # Create a new user object
        new_foods = ShrimpFoods.objects.create(
            food_name=food_name,
            food_description=food_description,
            food_image=food_image,
            allow_show=allow_show,
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
        if 'food_image' in request.FILES:
            foods.food_image = request.FILES['food_image']
        foods.allow_show = request.POST.get('allow_show')
        user_id = request.POST.get('userid')
        foods.save()
        return redirect('shrimpFoods')
    else:
        foods = ShrimpFoods.objects.get(id=food_id)
        return render(request, 'customadmin/edit_shrimpFoods.html', {"foods": foods})

@staff_member_required
def delete_shrimpFoods(request, food_id):
    species = ShrimpFoods.objects.get(id=food_id)
    species.deleted_at = datetime.now()
    species.save()
    return redirect('shrimpFoods')   

###################
##shrimpDiseases###
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
        allow_show = request.POST.get('allow_show')
        user_id = request.POST.get('userid')

        # Create a new user object
        new_diseases = ShrimpDiseases.objects.create(
            disease_name=disease_name,
            disease_symptom=disease_symptom,
            disease_image=disease_image,
            disease_prevent=disease_prevent,
            disease_treat=disease_treat,
            disease_cause=disease_cause,
            allow_show=allow_show,
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
        if 'disease_image' in request.FILES:
            disease.disease_image = request.FILES['disease_image']
        disease.disease_prevent = request.POST.get('disease_prevent')
        disease.disease_treat = request.POST.get('disease_treat')
        disease.disease_cause = request.POST.get('disease_cause')
        disease.allow_show = request.POST.get('allow_show')
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
    disease.deleted_at = datetime.now()
    disease.save()
    return redirect('shrimpDiseases')

###################
####shrimpPrice####
###################

@staff_member_required
def shrimpprice(request):
    price = ShrimpPrices.objects.filter(deleted_at=None)
    return render(request, 'customadmin/shrimpprice.html', {'price' : price})

@staff_member_required
def delete_shrimp_price(request, id):
    price = ShrimpPrices.objects.get(id=id)
    price.deleted_at = datetime.now()
    price.save()
    return redirect('shrimpprice.ad')

###################
####shrimpPond#####
###################

@staff_member_required
def shrimppond(request):
    pond = ShrimpPonds.objects.filter(deleted_at=None)
    return render(request, 'customadmin/shrimppond.html', {'pond' : pond})

###################
####Information####
###################
@staff_member_required
def information(request):
    information = Information.objects.filter(deleted_at=None)
    return render(request, 'customadmin/information.html', {'information' : information})

@staff_member_required
def add_information(request):
    if request.method == 'POST':
        information_name = request.POST.get('information_name')
        information_description = request.POST.get('information_description')
        allow_show = request.POST.get('allow_show')
        information_image = request.FILES.get('information_image')
        user_id = request.POST.get('userid')

        # Create a new user object
        new_diseases = Information.objects.create(
            information_name=information_name,
            information_description=information_description,
            allow_show=allow_show,
            information_image=information_image,
            user_id=user_id
        )
        return redirect('information')
    
    elif request.method == 'GET':
        return render(request, 'customadmin/add_information.html') 

@staff_member_required
def edit_information(request, information_id):
    if request.method == 'POST':
        information = Information.objects.get(id=information_id)
        information.information_name = request.POST.get('information_name')
        information.information_description = request.POST.get('information_description')
        if 'information_image' in request.FILES:
            information.information_image = request.FILES.get('information_image')
        information.allow_show = request.POST.get('allow_show')
        user_id = request.POST.get('userid')
        information.user_id = user_id
        information.save()
        return redirect('information')
    else:
        information = Information.objects.get(id=information_id)
        return render(request, 'customadmin/edit_information.html', {"information": information})


@staff_member_required
def delete_information(request, information_id):
    information = Information.objects.get(id=information_id)
    information.deleted_at = datetime.now()
    information.save()
    return redirect('information')

###################
## Water_quality ##
###################
@staff_member_required
def Water_quality(request):
    Water_quality = water_quality.objects.filter(deleted_at=None)
    return render(request, 'customadmin/water_quality.html', {'Water_quality' : Water_quality})

@staff_member_required
def add_water_quality(request):
    if request.method == 'POST':
        quality_name = request.POST.get('quality_name')
        quality_description = request.POST.get('quality_description')
        user_id = request.POST.get('userid')

        # Create a new user object
        new_quality = water_quality.objects.create(
            quality_name=quality_name,
            quality_description=quality_description,
            user_id=user_id
        )
        return redirect('water_quality')
    
    elif request.method == 'GET':
        return render(request, 'customadmin/add_water_quality.html') 

@staff_member_required
def edit_water_quality(request, water_id):
    if request.method == 'POST':
        Water_quality = water_quality.objects.get(id=water_id)
        Water_quality.quality_name = request.POST.get('quality_name')
        Water_quality.quality_description = request.POST.get('quality_description')
        user_id = request.POST.get('userid')
        Water_quality.user_id = user_id
        Water_quality.save()
        return redirect('water_quality')
    else:
        Water_quality = water_quality.objects.get(id=water_id)
        return render(request, 'customadmin/edit_water_quality.html', {"Water_quality": Water_quality})


@staff_member_required
def delete_water_quality(request, water_id):
    Water_quality = water_quality.objects.get(id=water_id)
    Water_quality.deleted_at = datetime.now()
    Water_quality.save()
    return redirect('water_quality')