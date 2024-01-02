import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def shrimptypes(request):
    return render(request, 'app_shrimp_type/shrimptypes.html')

def shrimptype(request, shrimp_id):
   d = {'col1': [1, 2], 'col2': [3, 4]}
   df = pd.DataFrame(data=d)
   return render(request, 'app_shrimp_type/shrimptypes.html', context={"shrimp_id": shrimp_id,"df":df})

