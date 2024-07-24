import requests
from django.shortcuts import render
from app_model.models import ShrimpPrices
from django.http import JsonResponse
from datetime import datetime, timedelta
from pytz import timezone
# ML import zone
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error

thai_months = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
]

def predict(yearY,monthY):
    df = pd.read_csv("media/extra/data_2.csv", encoding='tis-620')

    df[["date","XOX"]] = df.date.str.split("T", expand=True)
    df=df.drop(columns=[ 'XOX'], axis=1)
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
    selected_date = request.GET.get('calendar')
    yearX = request.GET.get('yearX')
    monthX = request.GET.get('monthX')

    if selected_date:
        api_url = f"https://dataapi.moc.go.th/gis-product-prices?product_id=P12004&from_date={selected_date}&to_date={selected_date}"
        
        try:
            response = requests.get(api_url)
            data = response.json()
            if 'price_list' in data:
                for price_entry in data['price_list']:
                    date_str = price_entry['date']
                    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone('Asia/Bangkok'))
                    date += timedelta(days=1)
                    formatted_date_str = date.strftime('%Y-%m-%d %H:%M:%S')
                    price_min = price_entry['price_min']
                    price_max = price_entry['price_max']
                    entry = ShrimpPrices.objects.filter(date=date).first()
                    if not entry:
                        shrimp_price = ShrimpPrices.objects.create(
                            price_specie=data.get('product_name'), 
                            price_min=price_min,
                            price_max=price_max,
                            date=date,  
                        )
                        shrimp_price.save()
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        except ValueError as e:
            return JsonResponse({'error': 'Invalid JSON format in API response'}, status=500)
    else:
        data = None
    
    if yearX and monthX:
        yearX= int(yearX)
        monthX = int(monthX)
        score,MSE,MAE,Predictt = predict(yearX,monthX)
    else:
        score = None
        MSE = None
        MAE = None
        Predictt = None

    return render(request, 'app_shrimp_price/shrimp_price.html',{'data': data,"score":score,"MSE":MSE,"MAE":MAE,"pre":Predictt,"M":monthX})












# def predictprice(request):
#     yearX = request.GET.get('yearX')
#     monthX = request.GET.get('monthX')
#     if yearX and monthX:
#         yearX= int(yearX)
#         monthX = int(monthX)
#         score,MSE,MAE,Predictt = predict(yearX,monthX)
#     else:
#         score = None
#         MSE = None
#         MAE = None
#         Predictt = None

#     return render(request, 'app_shrimp_price/shrimp_price.html', {"score":score,"MSE":MSE,"MAE":MAE,"pre":Predictt,"M":monthX})