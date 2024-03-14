from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from app_model.models import ShrimpPonds, ShrimpPondsDetail
# Create your views here.

def shrimppool(request,user_id):
    pool = ShrimpPonds.objects.all()
    user = User.objects.get(id=user_id)
    context = {'pool': pool,'user':user}
    return render(request,'app_shrimp_pool/shrimp_pool.html' , context)


def create_shrimppool(request ,user_id):
    if request.method == 'POST':
        pond_name = request.POST.get('pond_name')
        user_id = int(user_id)

        new_pool = ShrimpPonds.objects.create(
            pond_name = pond_name,
            user_id = user_id,
            
        )
        return redirect('shrimpool_dashbord', user_id=user_id)
    
    elif request.method == 'GET':
        return render(request, 'app_shrimp_pool/add_shrimp_pool.html') 