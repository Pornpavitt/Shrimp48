from django.urls import path
from . import views
# from app_shrimp_pool.urls import path
# from app_shrimp_pool.views import *
urlpatterns = [
    path('', views.home, name='home'),
    path('howtouse',views.howtouse, name='howtouse'),
    path('shrimp_diseases', views.shrimp_diseases, name='shrimp_diseases'),
    path('shrimp_food', views.shrimp_food, name='shrimp_food'),
    path('shrimp_species', views.shrimp_species, name='shrimp_species'),
    path('homeold', views.hometest , name='hometest')
]   