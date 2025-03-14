from django.urls import path , include
from . import views


urlpatterns = [
   path('',include("django.contrib.auth.urls")),
   path('register', view = views.register, name="register"),
   path('userprofile/<int:user_id>/', view = views.userprofile, name="userprofile"),
   path('eprofile/<int:user_id>/',views.edit_user_profile, name="euserprofile")
   
]