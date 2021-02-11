from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('files/', views.all_files, name='all_files'),
    re_path(r'^upload/get_link/$',
            views.get_upload_link, name='get_upload_link'),

]
