from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('howtouse',views.howtouse, name='howtouse ')
]