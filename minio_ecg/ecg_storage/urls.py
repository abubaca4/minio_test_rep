from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add_list'),
    path('add/file/', views.add_ecg_file, name='add_ecg_file_page')
]
