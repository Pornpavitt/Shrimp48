import requests
from django.shortcuts import render
from app_model.models import ShrimpPrices
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Max
# ML import zone
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error


def predict(yearY,monthY):
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

    y_predict = model.predict(x_poly)
    plt.scatter(x.ravel(), y, color='b')
    plt.plot(x.ravel(), y_predict, linewidth='2', color='r')
    # plt.show()

    dp["predict"] = y_predict
    score = model.score(x_poly,y)
    MSE = mean_squared_error(y, y_predict)
    MAE = mean_absolute_error(y, y_predict)
    print('score',score)
    print('MSE',MSE)
    print('MAE',MAE)
    y_predict_Future = model.predict(dfpoly.fit_transform([[monthY]]))
    print('Predict',y_predict_Future)
    return score,MSE,MAE,y_predict_Future


def shrimpprice(request):
    yearX = request.GET.get('yearX')
    monthX = request.GET.get('monthX')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    latest_date = ShrimpPrices.objects.filter(
        deleted_at=None, 
        price_specie="กุ้งขาว (70 ตัว/กก.)" 
    ).aggregate(latest_date=Max('date'))['latest_date']
    shrimpprice_view = ShrimpPrices.objects.filter(deleted_at=None, date=latest_date)
    error_message = None

    # Initialize prediction variables
    score = None
    MSE = None
    MAE = None
    Predictt = None
    prediction_dates = []
    prediction_values = []
    y_predict_Future = []
    
    if yearX and monthX:
        yearX = int(yearX)
        monthX = int(monthX)
        score,MSE,MAE,Predictt = predict(yearX,monthX)
    else:
        score = None
        MSE = None
        MAE = None
        Predictt = None


    shrimp_prices = []
    shrimp_dates = []
    shrimp_prices_min = []
    shrimp_prices_max = []
    shrimp_prices_predict = []


    if start_date and end_date:
        try:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)  
            if start_datetime > end_datetime:
                error_message = "วันที่เริ่มต้นต้องไม่มากกว่าวันที่สิ้นสุด"
            else:
                shrimp_prices = ShrimpPrices.objects.filter(date__range=[start_datetime, end_datetime])
            for price in shrimp_prices:
                shrimp_dates.append(price.date.strftime('%Y-%m-%d'))
                shrimp_prices_min.append(float(price.price_min) if price.price_min else 0)
                shrimp_prices_max.append(float(price.price_max) if price.price_max else 0)
                shrimp_prices_predict.append(float(price.predict) if price.predict else 0)
        except ValueError:
            error_message = "รูปแบบวันที่ไม่ถูกต้อง"
            shrimp_prices = ShrimpPrices.objects.none()

    return render(request, 'app_shrimp_price/shrimp_price.html', {
        "shrimpprice_view":shrimpprice_view,
        "shrimp_prices": shrimp_prices,
        "shrimp_dates": shrimp_dates,
        "shrimp_prices_min": shrimp_prices_min,
        "shrimp_prices_max": shrimp_prices_max,
        "shrimp_prices_predict":shrimp_prices_predict,
        "score": score,
        "MSE": MSE,
        "MAE": MAE,
        "pre": Predictt,
        "prediction_dates": prediction_dates,
        "prediction_values": prediction_values,
        "M": monthX,
        "Y": yearX,
        "error_message": error_message,
        'start_date': start_date,
        'end_date': end_date,
        "y_predict" : y_predict_Future
    })




def shrimpprice_view(request):
    selected_date = request.GET.get('calendar') 
    
    if selected_date:
        shrimp_prices = ShrimpPrices.objects.filter(date=selected_date)
    else:
        shrimp_prices = ShrimpPrices.objects.none()  
    return render(request, 'app_shrimp_price/shrimp_price.html', {'shrimp_prices': shrimp_prices})

