from django.urls import path
from django.urls import re_path

from . import views


urlpatterns = [
    path('', views.index, name='ecg_index'),
    path('add/', views.add, name='list_of_avaliable_models_addition'),
    re_path(r'^add/file/$', views.add_ecg_file, name='add_ecg_file_page'),
    path('add/patient/', views.add_patient, name='add_patient_page'),
    path('list/', views.common_list, name='list_models_records'),
    path('list/ecg/', views.ecg_list, name='list_ecg_records'),
    path('view/file/<int:id>/', views.view_file, name='file_view'),
    path('view/file/<int:id>/download/',
         views.file_download_link, name='file_download'),
    path('view/patient/<int:id>/', views.view_patient, name='patient_view'),
]
