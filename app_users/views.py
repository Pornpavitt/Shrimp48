from django.contrib.auth import login
from django.http import HttpRequest ,HttpResponseRedirect
from django.shortcuts import render
from app_users.forms import RegisterForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

def register(request:HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request ,user)
            return HttpResponseRedirect(reverse("home"))
    else:
        form = RegisterForm()
    
    context = {'form' : form}
    return render(request,"app_users/register.html", context)


       