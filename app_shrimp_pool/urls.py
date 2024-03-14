from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dashbord/<user_id>', views.shrimppool , name="shrimpool_dashbord" ),
    path('add_shrimp_pool/<user_id>', views.create_shrimppool, name='add_shrimp_pool'),

]
