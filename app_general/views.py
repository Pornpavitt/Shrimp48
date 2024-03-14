from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    # user = User.objects.all()
    return render(request, 'app_general/home.html')

def howtouse(request):
    return render(request, 'app_general/howtouse.html')
