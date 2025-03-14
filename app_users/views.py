from django.contrib.auth import login
from django.http import HttpRequest ,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404 ,redirect
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

def userprofile(request, user_id):
    users =User.objects.filter(id=user_id)

    return render(request, "app_users/userprofile.html", {users:'users'})

    
def edit_user_profile(request, user_id):
    if request.method == 'POST':
        users = User.objects.get(id=user_id)
        users.first_name = request.POST['first_name']
        users.last_name = request.POST['last_name']
        if 'image' in request.FILES:
            users.image = request.FILES['image']
        users.save()
        return redirect('userprofile' ,user_id=user_id)
    else:
        users = User.objects.get(id=user_id)
        return render(request, 'app_users/edit_userprofile.html', {"users": users})
        