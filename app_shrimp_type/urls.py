from django.urls import path
from . import views

urlpatterns = [
    path('', views.shrimptypes, name='shrimptypes'),
    path('<int:shrimp_id>', views.shrimptype, name='shrimp')
]