from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def shrimptypes(request):
    return render(request, 'app_shrimp_type/shrimptypes.html')

def shrimptype(request, shrimp_id):
    return render(request, 'app_shrimp_type/shrimptypes.html', context={"shrimp_id": shrimp_id})