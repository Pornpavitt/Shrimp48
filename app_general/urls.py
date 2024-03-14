from django.urls import path
from . import views
# from app_shrimp_pool.urls import path
# from app_shrimp_pool.views import *
urlpatterns = [
    path('', views.home, name='home'),
    path('howtouse',views.howtouse, name='howtouse'),
    # path('eee/', views.eee , name="eee"),
    # path('add_shrimp_pool/<user_id>' , views.create_shrimppool)
]   