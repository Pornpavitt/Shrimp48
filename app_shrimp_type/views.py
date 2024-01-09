import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import ShrimpSpecies

all_shrimptypes = [
    {'id' : 1, 'title' : 'กุ้งขาว','Price': 2000000 , 'is_pop':True,'pop_end_at':datetime(2024,2,2)},
    {'id' : 2, 'title' : 'กุ้งกุลาดำ','Price': 200 , 'is_pop':True,'pop_end_at':datetime(2024,1,1)}
]

# Create your views here.


def shrimptypes(request):
    dbShrimp = ShrimpSpecies.objects.all()
    context = {'shrimptypes' : all_shrimptypes,'dbShrimp':dbShrimp}
    return render(request, 'app_shrimp_type/shrimptypes.html',context)

def shrimptype(request, shrimp_id):
    one_shrimp = None
    try:
        one_shrimp = [f for f in all_shrimptypes if f['id'] == shrimp_id ][0]
    except IndexError:
        print('ไม่มีข้อมูลในตอนี้')
    context = {'shrimp' : one_shrimp}
    return render(request, 'app_shrimp_type/shrimptype.html', context)

