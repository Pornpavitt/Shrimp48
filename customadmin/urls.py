from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.admin_login , name='login'),
    path('dashboard/', views.dashboard , name='dashboard'),
    path('create_shrimp_species/', views.create_shrimp_species, name='create_shrimp_species'),
    path('add_users/', views.add_users , name='add_users'),
    path('user/', views.user, name='user'),
    path('edit_user/<user_id>', views.edit_user, name='edit_user'),
    path('delete_user/<user_id>', views.delete_user, name='delete_user')

]

