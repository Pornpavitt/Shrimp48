from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.admin_login , name='login'),
    path('dashboard/', views.dashboard , name='dashboard'),

    #User
    path('user/', views.user, name='user'),
    path('add_users/', views.add_users , name='add_users'),
    path('edit_user/<user_id>', views.edit_user, name='edit_user'),
    path('delete_user/<user_id>', views.delete_user, name='delete_user'),

    #Species
    path('shrimpSpecies/', views.shrimpSpecies , name="shrimpSpecies"),
    path('add_species/',views.add_shrimpSpecies, name="add_shrimpSpecies"),
    path('edit_shrimpSpecies/<specie_id>', views.edit_species, name="edit_shrimpSpecies"),
    path('delete_species/<specie_id>' , views.delete_species, name="delete_species"),
    
    #Foods
    path('shrimpFoods/', views.shrimpFoods , name="shrimpFoods"),
    path('add_shrimpfood/',views.add_shrimpFoods, name="add_shrimpfood"),
    path('edit_shrimpFoods/<food_id>', views.edit_shrimpFoods, name='edit_shrimpFood'),
    path('delete_shrimpFoods/<food_id>' , views.delete_shrimpFoods, name="delete_shrimpFoods"),
    
    # Diseases
    path('shrimpDiseases/', views.shrimpDiseases, name="shrimpDiseases"),
    path('add_shrimpdisease/', views.add_shrimpDiseases, name="add_shrimpdisease"),
    path('edit_shrimpDisease/<disease_id>', views.edit_shrimp_diseases, name='edit_shrimpDisease'),
    path('delete_shrimpDisease/<disease_id>', views.delete_shrimp_diseases, name="delete_shrimpDisease"),

   
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
