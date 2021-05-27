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
    path("api/auth/", views.api_login, name="json_login"),
    path('api/ecg/list/', views.api_ecg_list, name='json_ecg_list'),
    path('api/ecg/add/', views.api_add_ecg, name='json_ecg_add'),
    path('api/ecg/<int:id>/info/', views.api_ecg_info, name='json_ecg_info'),
    path('api/ecg/<int:id>/edit/', views.api_edit_ecg, name='json_ecg_edit'),
    path('api/file/list/', views.api_file_list, name='json_file_list'),
    path('api/file/add/', views.api_add_ecg_file, name='json_file_add'),
    path('api/file/<int:id>/info/', views.api_file_info, name='json_file_info'),
    path('api/file/<int:id>/edit/', views.api_edit_ecg_file, name='json_file_edit'),
    path('api/patient/list/', views.api_patient_list, name='json_patient_list'),
    path('api/patient/add/', views.api_add_patient, name='json_patient_add'),
    path('api/patient/<int:id>/info/',
         views.api_patient_info, name='json_patient_info'),
    path('api/patient/<int:id>/edit/',
         views.api_edit_patient, name='json_patient_edit'),
    path('api/source_org/list/', views.api_source_org_list,
         name='json_source_org_list'),
    path('api/source_org/<int:id>/info/',
         views.api_source_org_info, name='json_source_org_info'),
    path('api/original_information/list/', views.api_original_information_list,
         name='json_original_information_list'),
    path('api/original_information/add/', views.api_add_original_information,
         name='json_original_information_add'),
    path('api/original_information/<int:id>/info/',
         views.api_original_information_info, name='json_original_information_info'),
    path('api/access_groups/list/', views.api_access_groups_list,
         name='json_access_groups_list'),
]
