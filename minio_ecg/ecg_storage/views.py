from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from .models import ecg
from .models import ecg_files

from .forms import FileUploadForm
from .forms import PatientForm

from datetime import timedelta

# Create your views here.


def index(request: HttpRequest):
    return render(
        request,
        'index.html',
        context={},
    )


def common_list(request: HttpRequest):
    return render(
        request,
        'list_of_lists.html',
        context={},
    )


def add(request: HttpRequest):
    return render(
        request,
        'add_list.html',
        context={},
    )


def ecg_list(request: HttpRequest):
    return render(
        request,
        'ecg_list.html',
        context={'ecg_list': ecg.objects.all()},
    )


def view_file(request: HttpRequest, id: int):
    file_obj = get_object_or_404(ecg_files, id=id)
    return render(
        request,
        'file_view.html',
        context={'o_file': file_obj},
    )


@login_required
def add_ecg_file(request: HttpRequest):
    if request.method == 'POST':
        form = FileUploadForm(request.POST)
        if form.is_valid():
            dict_response = {}
            new_ecg_file = form.make_obj_from_form()
            new_ecg_file.save()
            dict_response['upload_url'] = new_ecg_file.get_minio_upload_link(
                link_live_duration=timedelta(minutes=5))
            dict_response['ecg_file_id'] = new_ecg_file.id
            dict_response['redirect_url'] = new_ecg_file.get_absolute_url()
            return JsonResponse(dict_response)
        else:
            data = form.errors
            return JsonResponse(data, status=400, safe=False)
    else:
        ecg_id = request.GET.get('ecg_id', '')
        sample_frequency = request.GET.get('sample_frequency', '')
        amplitude_resolution = request.GET.get('amplitude_resolution', '')
        form = FileUploadForm(initial={'ecg_id_field': ecg_id, 'sample_frequency_field': sample_frequency,
                                       'amplitude_resolution_field': amplitude_resolution})
        return render(
            request,
            'upload_file.html',
            context={'form': form, 'page_title': 'Добаление ecg файла'},
        )


def file_download_link(request: HttpRequest, id: int):
    file_obj = get_object_or_404(ecg_files, id=id)
    # добавить проверку на доступ к файлу
    return redirect(file_obj.get_minio_download_link(link_live_duration=timedelta(minutes=5)))


def add_patient(request: HttpRequest):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return
    else:
        form = PatientForm()

    return render(request, 'add_patient.html', context={'form': form},)
