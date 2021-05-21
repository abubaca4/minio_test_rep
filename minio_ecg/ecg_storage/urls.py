from django.urls import path
from django.urls import re_path

from . import views


urlpatterns = [
    path('', views.index, name='ecg_index'),
    path('add/', views.add_list, name='list_of_avaliable_models_addition'),
    path('list/', views.common_list, name='list_models_records'),
]

urlpatterns += [
    re_path(r'^add/file/$', views.add_ecg_file, name='add_ecg_file_page'),
    path('add/patient/', views.add_patient, name='add_patient_page'),
    path('add/ecg/', views.add_ecg, name='add_ecg_page'),
]

urlpatterns += [
    path('list/ecg/', views.ecg_list, name='list_ecg_records'),
    path('list/file/', views.file_list, name='list_files'),
]

urlpatterns += [
    path('view/file/<int:id>/', views.view_file, name='file_view'),
    path('view/file/<int:id>/download/',
         views.file_download_link, name='file_download'),
    path('view/ecg/<int:id>/', views.view_ecg, name='ecg_view'),
    path('view/patient/<int:id>/', views.view_patient, name='patient_view'),
]

urlpatterns += [
    path('edit/patient/<int:id>/', views.edit_patient, name='patient_edit'),
    path('edit/file/<int:id>/', views.edit_file, name='file_edit'),
    path('edit/ecg/<int:id>/', views.edit_ecg, name='ecg_edit'),
]

urlpatterns += [
    path('api/ecg_list/', views.api_ecg_list, name='json_ecg_list'),
    
]
