from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    user = User.objects.first()
    if user:
        user_name = user.username
    else:
        user_name = "Guest" 

    context = {'user_name': user_name}
    return render(request, 'app_general/home.html',context)

def howtouse(request):
    return render(request, 'app_general/howtouse.html')