from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('product-prices/', views.shrimpprice, name='shrimpprice'),
   # path('shrimp-price/', views.shrimp_price_view, name='price_view'),
]
