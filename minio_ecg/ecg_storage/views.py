from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import ecg
from .models import ecg_files

from .forms import FileUpload

from datetime import timedelta

# Create your views here.


def index(request):
    return render(
        request,
        'index.html',
        context={},
    )


def add(request):
    return render(
        request,
        'add_list.html',
        context={},
    )


@login_required
def add_ecg_file(request):
    if request.method == 'POST':
        dict_response = {}
        form = FileUpload(request.POST)
        if form.is_valid():
            dict_response['data'] = form.cleaned_data
            return JsonResponse(dict_response, safe=False)
        else:
            data = form.errors
            return JsonResponse(data, status=400, safe=False)
    else:
        return render(
            request,
            'upload_file.html',
            context={},
        )


def common_list(request):
    return render(
        request,
        'list_of_lists.html',
        context={},
    )


def ecg_list(request):
    return render(
        request,
        'ecg_list.html',
        context={'ecg_list': ecg.objects.all()},
    )


@login_required
def get_minio_upload_link(request):
    dict_response = {'is_error': False, 'error_text': '',  'upload_url': ''}

    file_name = request.GET.get('file_name', None)
    ecg_id = request.GET.get('ecg_id', None)
    format = request.GET.get('format', None)
    sample_frequency = request.GET.get('sample_frequency', None)
    amplitude_resolution = request.GET.get('amplitude_resolution', None)

    if file_name == None or ecg_id == None or format == None or sample_frequency == None or amplitude_resolution == None:
        dict_response['is_error'] = True
        dict_response['error_text'] = 'Получены не все неообходимые данные'

    if not dict_response['is_error']:
        if ecg_files.objects.filter(file_name=file_name).count() != 0:
            dict_response['is_error'] = True
            dict_response['error_text'] = 'Такой файл уже существует'
    
    def isNum(data):
        try:
            int(data)
            return True
        except ValueError:
            return False

    if not dict_response['is_error']:
        if not isNum(sample_frequency):
            dict_response['is_error'] = True
            dict_response['error_text'] = 'Sample frequency не целое число'

    if not dict_response['is_error']:
        if not isNum(amplitude_resolution):
            dict_response['is_error'] = True
            dict_response['error_text'] = 'Amplitude resolution не целое число'

    if not dict_response['is_error']:
        if not isNum(ecg_id):
            dict_response['is_error'] = True
            dict_response['error_text'] = 'ID экг не целое число'

    if not dict_response['is_error']:
        if ecg.objects.filter(id=int(ecg_id)).count() == 0:
            dict_response['is_error'] = True
            dict_response['error_text'] = 'Экг с таким ID не существует'

    if not dict_response['is_error']:
        new_ecg_file = ecg_files(ecg_id = int(ecg_id), format = format, file_name = file_name, sample_frequency = int(sample_frequency), amplitude_resolution = int(amplitude_resolution))
        dict_response['upload_url'] = new_ecg_file.get_minio_upload_link(link_live_duration=timedelta(minutes=5))
        new_ecg_file.save()

    return JsonResponse(dict_response)
