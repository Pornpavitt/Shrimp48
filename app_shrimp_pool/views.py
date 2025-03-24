from django.shortcuts import render ,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseNotAllowed
from django.contrib.auth.models import User
from app_model.models import ShrimpPonds, ShrimpPondsDetail, ShrimpPrices, water_quality
from datetime import datetime, timedelta
# Create your views here.

def shrimppool(request, user_id):
    user = User.objects.filter(id=user_id).first()
    ponds = ShrimpPonds.objects.filter(user_id=user_id,deleted_at = None)
    pool_details = ShrimpPondsDetail.objects.filter(pond_id__in=ponds.values_list('id')).order_by('-created_at') 
    water = water_quality.objects.filter(deleted_at=None)
    context = {
        'ponds': ponds,
        'user': user,
        'pool_details': pool_details,
        'water':water
    }
    return render(request, 'app_shrimp_pool/shrimp_pool.html', context)


def create_shrimppool(request, user_id):
    if request.method == 'POST':
        pond_name = request.POST.get('pond_name')
        user_id = int(user_id)
        pond_address = request.POST.get('pond_address')
        pond_number = request.POST.get('pond_number')
        pond_image = request.FILES.get('pond_image')
        
        new_pool = ShrimpPonds.objects.create(
            pond_name=pond_name,
            user_id=user_id,
            pond_address=pond_address,
            pond_number=pond_number,
            pond_image=pond_image
        )
        return redirect('shrimpool_dashbord', user_id=user_id)
    
    elif request.method == 'GET':
        return render(request, 'app_shrimp_pool/shrimp_pool.html')
    
    
def delete_pool(request, pond_id, user_id):
    pond = get_object_or_404(ShrimpPonds, id=pond_id)
    pond.deleted_at  = datetime.now()
    pond.save()
    return redirect('shrimpool_dashbord', user_id=user_id)

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error

def load_model():
    df = pd.read_csv('media/extra/test.csv')
    df2 =df.drop(columns=['GrowthGrade','SurvivalRate(%)','SurvivalGrade'])
    x = df2[['DO(mg/L)', 'Temp(*C)', 'pH', 'Transparency(cm)', 'salinity(ppt)', 'alkalinity(Mg/l_as_CaCO3)', 'nitrite(Mg/L)', 'hardness(Mg/L)', 'TAN(Mg/l)']].values
    y = df2['GrowthRate(adg)'].values
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=1)
    rg = DecisionTreeRegressor()
    rg.fit(x_train, y_train)
    y_predict = rg.predict(x_test)
    MAE = mean_absolute_error(y_test,y_predict)
    return rg

growth_rate_model = load_model()

def load_dateG():
    data_import = pd.read_csv('media/extra/test2.csv')
    data_import1 = data_import.drop(columns=[ 'Cal','cal','Unnamed: 9','Unnamed: 10'], axis=1)
    x = data_import1['age(day)'].values.reshape(-1,1)
    dfpoly = PolynomialFeatures(degree=2)
    x_poly = dfpoly.fit_transform(x)
    y = data_import1['growth rate (adg)']
    plr = LinearRegression()
    plr.fit(x_poly,y)
    return plr, dfpoly

growth_dateG_model = load_dateG()

def load_weightG():
    data_import = pd.read_csv('media/extra/test2.csv')
    data_import2 = data_import.drop(columns=[ 'Cal','cal','Unnamed: 9','Unnamed: 10'], axis=1)
    x = data_import2['weight(g.)'].values.reshape(-1,1)
    dfpoly = PolynomialFeatures(degree=2)
    x_poly = dfpoly.fit_transform(x)
    y = data_import2['growth rate (adg)']
    plr = LinearRegression()
    plr.fit(x_poly,y)
    return plr, dfpoly

growth_weightG_model = load_weightG()

def load_survival():
    df = pd.read_csv('media/extra/test.csv')
    df4 =df.drop(columns=['GrowthGrade','GrowthRate(adg)','SurvivalGrade'])
    x=df4[['DO(mg/L)', 'Temp(*C)', 'pH', 'Transparency(cm)', 'salinity(ppt)', 'alkalinity(Mg/l_as_CaCO3)', 'nitrite(Mg/L)', 'hardness(Mg/L)', 'TAN(Mg/l)']].values
    y=df4[['SurvivalRate(%)']].values
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=1)
    rg = DecisionTreeRegressor()
    rg.fit(x_train,y_train)
    return rg

survival_rate_model = load_survival()

def cal_food (w,q):
    if w >= 0 and w < 0.5  :
        FW = 2*(q/100000)*1000
        return FW
    elif w >= 0.5 and w < 3 :
        FW = w*4*(q/100000)*1000
        return FW
    elif w >= 3 and w < 4 :
        FW = w*4.4*(q/100000)*1000
        return FW
    elif w >= 4 and w < 5 :
        FW = w*3.7*(q/100000)*1000
        return FW
    elif w >= 5 and w < 7 :
        FW = w*3.5*(q/100000)*1000
        return FW
    elif w >= 7 and w < 8 :
        FW = w*3.3*(q/100000)*1000
        return FW
    elif w >= 8 and w < 9 :
        FW = w*3*(q/100000)*1000
        return FW
    elif w >= 9 and w < 11 :
        FW = w*2.8*(q/100000)*1000
        return FW
    elif w >= 11 and w < 12 :
        FW = w*2.7*(q/100000)*1000
        return FW
    elif w >= 12 and w < 14 :
        FW = w*2.5*(q/100000)*1000
        return FW
    elif w >= 14 and w < 16 :
        FW = w*2.3*(q/100000)*1000
        return FW
    elif w >= 16 and w < 18 :
        FW = w*2.2*(q/100000)*1000
        return FW
    elif w >= 18 and w < 22 :
        FW = w*2.1*(q/100000)*1000
        return FW
    elif w >= 22 :
        FW = w*2*(q/100000)*1000
        return FW


def pool_detail(request, pond_id):
    pond = get_object_or_404(ShrimpPonds, id=pond_id)
    pond_details = ShrimpPondsDetail.objects.filter(pond_id=pond_id).order_by('-created_at')
    water = water_quality.objects.filter(deleted_at=None)
    predicted_growth_rate_dateG = None
    predicted_growth_rate_weightG = None
    predicted_survival_rate = None
    predicted_growth_rate = None
    foodqura=None
    
    details = ShrimpPondsDetail.objects.filter(pond_id=pond_id).order_by('-created_at')[:2]
    if len(details) > 0:
        first_detail = details[0]
        foodqura = cal_food(first_detail.shrimp_weight,first_detail.shrimp_quantity)
    if len(details) > 1:
        second_detail = details[1] 
        
        def get_color(value1, value2):
            if value1 > value2:
                return 'green'
            elif value1 < value2:
                return 'red'
            else:
                return 'gray'  

        data_dissolvedOxygen = {
            'value': first_detail.pond_dissolvedOxygen - second_detail.pond_dissolvedOxygen if second_detail else 0,
            'color': get_color(first_detail.pond_dissolvedOxygen, second_detail.pond_dissolvedOxygen) if second_detail else 'gray'
        }

        data_pH = {
            'value': first_detail.pond_pH - second_detail.pond_pH if second_detail else 0,
            'color': get_color(first_detail.pond_pH, second_detail.pond_pH) if second_detail else 'gray'
        }

        data_salinity = {
            'value': first_detail.salinity - second_detail.salinity if second_detail else 0,
            'color': get_color(first_detail.salinity, second_detail.salinity) if second_detail else 'gray'
        }

        data_alkalinity = {
            'value': first_detail.alkalinity - second_detail.alkalinity if second_detail else 0,
            'color': get_color(first_detail.alkalinity, second_detail.alkalinity) if second_detail else 'gray'
        }

        data_nitrite = {
            'value': first_detail.nitrite - second_detail.nitrite if second_detail else 0,
            'color': get_color(first_detail.nitrite, second_detail.nitrite) if second_detail else 'gray'
        }

        data_TAN = {
            'value': first_detail.TAN - second_detail.TAN if second_detail else 0,
            'color': get_color(first_detail.TAN, second_detail.TAN) if second_detail else 'gray'
        }
        data_growth = {
            'value': first_detail.growth_rate - second_detail.growth_rate if second_detail else 0,
            'color': get_color(first_detail.growth_rate,second_detail.growth_rate) if second_detail else 'gray'
        }
        last_growth = {
            'value' : first_detail.growth_rate if first_detail else 0,
        }
    else:
        data_dissolvedOxygen = data_pH = data_salinity = data_alkalinity = data_nitrite = data_TAN = data_growth = last_growth = None

    if request.method == 'POST':
        if 'create_shrimp_pool_detail' in request.POST:
            # Collect form data for shrimp pool detail
            pond_id = request.POST.get('pond_id')
            shrimp_quantity = request.POST.get('shrimp_quantity')
            shrimp_weight = request.POST.get('shrimp_weight')
            pond_dissolvedOxygen = request.POST.get('pond_dissolvedOxygen')
            pond_waterHardness = request.POST.get('pond_waterHardness')
            pond_pH = request.POST.get('pond_pH')
            pond_temperature = request.POST.get('pond_temperature')
            food_quantity = request.POST.get('food_quantity')
            survival_rate = request.POST.get('survival_rate')
            total_date = request.POST.get('total_date')
            TAN = request.POST.get('TAN')
            alkalinity = request.POST.get('alkalinity')
            nitrite = request.POST.get('nitrite')
            salinity = request.POST.get('salinity')
            transparency = request.POST.get('transparency')
            
            growth_rate = 0 
            previous_detail = ShrimpPondsDetail.objects.filter(pond_id=pond_id).order_by('-created_at').first()
            
            if previous_detail:
                shrimp_weight_previous = float(previous_detail.shrimp_weight)
                date_previous = int(previous_detail.total_date)

                
                shrimp_weight = float(request.POST.get('shrimp_weight'))  
                shrimp_quantity = request.POST.get('shrimp_quantity')
                total_date = int(request.POST.get('total_date'))
                delta_weight = shrimp_weight - shrimp_weight_previous
                delta_days = total_date - date_previous
                
                
                if delta_days > 0:
                    growth_rate = delta_weight / delta_days

            input_data = [
                float(pond_dissolvedOxygen),
                float(pond_temperature),
                float(pond_pH),
                float(transparency),
                float(salinity),
                float(alkalinity),
                float(nitrite),
                float(pond_waterHardness),
                float(TAN),
            ]

            
            growth_dateG_model, dfpoly = load_dateG()
            growth_weightG_model, dfpoly = load_weightG()
            try:
                
                x_polyD = dfpoly.transform([[total_date]])
                predicted_growth_rate_dateG = growth_dateG_model.predict(x_polyD)[0]
                
                x_polyW = dfpoly.transform([[shrimp_weight]])
                predicted_growth_rate_weightG = growth_weightG_model.predict(x_polyW)[0]
                
                predicted_growth_rate = growth_rate_model.predict([input_data])[0]
                
                predicted_survival_rate = survival_rate_model.predict([input_data])[0]
            except ValueError:
                predicted_growth_rate = None  
                predicted_growth_rate_dateG = None
                predicted_growth_rate_weightG = None
                predicted_survival_rate = None


            ShrimpPondsDetail.objects.create(
                pond_id=pond_id,
                shrimp_quantity=shrimp_quantity,
                shrimp_weight=shrimp_weight,
                pond_dissolvedOxygen=pond_dissolvedOxygen,
                pond_waterHardness=pond_waterHardness,
                pond_pH=pond_pH,
                pond_temperature=pond_temperature,
                food_quantity=food_quantity,
                growth_rate=growth_rate,
                predicted_growth_rate=predicted_growth_rate,#Predict
                survival_rate=predicted_survival_rate,#Predict
                total_date=total_date,
                TAN=TAN,
                alkalinity=alkalinity,
                nitrite=nitrite,
                salinity=salinity,
                transparency=transparency,
                predicted_growth_rate_date_base=predicted_growth_rate_dateG,
                predicted_growth_rate_weight_base = predicted_growth_rate_weightG
            )
            return redirect('pond_detail', pond_id=pond_id)
        


    context = {
        'pond': pond,
        'pond_details': pond_details,
        'latest_detail_id': first_detail.id if len(details) > 0 else None,  
        'data_dissolvedOxygen': data_dissolvedOxygen,
        'data_pH': data_pH,
        'data_salinity': data_salinity,
        'data_alkalinity': data_alkalinity,
        'data_nitrite': data_nitrite,
        'data_TAN': data_TAN,
        'foodqura':foodqura,
        'data_growth':data_growth,
        'water':water,
        'last_growth':last_growth
        

    }

    return render(request, 'app_shrimp_pool/shrimp_pool_detail.html', context)






