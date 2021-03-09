from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='ecg_index'),
    path('add/', views.add, name='list_of_avaliable_models_addition'),
    path('add/file/', views.add_ecg_file, name='add_ecg_file_page'),
    path('list/', views.common_list, name='list_models_records'),
]
