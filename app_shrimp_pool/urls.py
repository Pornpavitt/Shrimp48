from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashbord/<user_id>', views.shrimppool , name="shrimpool_dashbord" ),
    path('add_shrimp_pool/<user_id>', views.create_shrimppool, name='add_shrimp_pool'),
    path('delete_pool/<int:pond_id>/<int:user_id>' , views.delete_pool , name="delete_pool"),
    path('pond_detail/<pond_id>',views.pool_detail,name="pond_detail")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
