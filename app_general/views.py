from django.shortcuts import render
from django.http.response import HttpResponse
# from app_model.models import Users

# Create your views here.
def home(request):
    # user = Users.objects.first()
    # if user:
    #     user_name = user.user_FName
    # else:
    #     user_name = "Guest" 

    # context = {'user_name': user_name}
    return render(request, 'app_general/home.html')

def howtouse(request):
    return render(request, 'app_general/howtouse.html')