from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from .models import ecg
from .models import ecg_files
from .models import patients
from .models import access_groups
from .models import source_org
from .models import original_information

from .forms import FileUploadForm
from .forms import PatientForm
from .forms import EcgForm
from .forms import FileEditForm
from .forms import OriginalInformation

from datetime import timedelta

# Create your views here.


def get_ForeginKey_id_or_empty(key):
    try:
        id = key.id
    except AttributeError:
        id = None
    return id


def index(request: HttpRequest):
    return render(
        request,
        'common_pages/index.html',
        context={'page_title': 'Хранилище экг'},
    )


def common_list(request: HttpRequest):
    return render(
        request,
        'common_pages/list_of_lists.html',
        context={'page_title': 'Списки записей'},
    )


def add_list(request: HttpRequest):
    return render(
        request,
        'common_pages/add_list.html',
        context={'page_title': 'Добавление новых записей'},
    )


def ecg_list(request: HttpRequest):
    form = EcgForm()
    return render(
        request,
        'list_pages/ecg_list.html',
        context={'ecg_list': ecg.objects.all(
        ), 'page_title': 'Список доступных экг', 'form': form},
    )


def api_ecg_list(request: HttpRequest):
    resp_dict = {}
    query = ecg.objects

    check_date = False
    add_date = False
    patient_age = False
    patient_id = False
    source_user = False
    access_id = False
    org_id = False

    field_list = request.GET.get('fields', '').split(',')

    if 'check_date' in field_list:
        check_date = True

    if 'add_date' in field_list:
        add_date = True

    if 'patient_age' in field_list:
        patient_age = True

    if 'patient_id' in field_list:
        patient_id = True
        query.select_related("patient_id")

    if 'source_user' in field_list:
        source_user = True
        query.select_related("source_user")

    if 'access_id' in field_list:
        access_id = True
        query.select_related("access_id")

    if 'org_id' in field_list:
        org_id = True
        query.select_related("org_id")

    j = 0
    for i in query.all():
        resp_dict[j] = {'id': i.id}
        if check_date:
            resp_dict[j]['check_date'] = i.check_date
        if add_date:
            resp_dict[j]['add_date'] = i.add_date
        if patient_age:
            resp_dict[j]['patient_age'] = i.patient_age
        if patient_id:
            resp_dict[j]['patient_id'] = get_ForeginKey_id_or_empty(
                i.patient_id)
        if source_user:
            resp_dict[j]['source_user'] = get_ForeginKey_id_or_empty(
                i.source_user)
        if access_id:
            resp_dict[j]['access_id'] = get_ForeginKey_id_or_empty(i.access_id)
        if org_id:
            resp_dict[j]['org_id'] = get_ForeginKey_id_or_empty(i.org_id)
        j += 1

    return JsonResponse(resp_dict, safe=False)


def file_list(request: HttpRequest):
    form = FileUploadForm()
    return render(
        request,
        'list_pages/file_list.html',
        context={'form': form, 'file_list': ecg_files.objects.select_related("ecg_id").all(
        ), 'page_title': 'Список доступных экг файлов'},
    )


def api_file_list(request: HttpRequest):
    resp_dict = {}
    query = ecg_files.objects

    ecg_id = False
    format = False
    file_hash = False
    sample_frequency = False
    amplitude_resolution = False
    original_name = False

    field_list = request.GET.get('fields', '').split(',')

    if 'ecg_id' in field_list:
        ecg_id = True
        query.select_related("ecg_id")

    if 'format' in field_list:
        format = True

    if 'file_hash' in field_list:
        file_hash = True

    if 'sample_frequency' in field_list:
        sample_frequency = True

    if 'amplitude_resolution' in field_list:
        amplitude_resolution = True

    if 'original_name' in field_list:
        original_name = True

    j = 0
    for i in query.all():
        resp_dict[j] = {'id': i.id}
        if ecg_id:
            resp_dict[j]['ecg_id'] = i.ecg_id.id
        if format:
            resp_dict[j]['ecg_id'] = i.format
        if file_hash:
            resp_dict[j]['file_hash'] = i.file_hash
        if sample_frequency:
            resp_dict[j]['sample_frequency'] = i.sample_frequency
        if amplitude_resolution:
            resp_dict[j]['amplitude_resolution'] = i.amplitude_resolution
        if original_name:
            resp_dict[j]['original_name'] = i.original_name
        j += 1

    return JsonResponse(resp_dict, safe=False)


def api_patient_list(request: HttpRequest):
    resp_dict = {}
    j = 0
    for i in patients.objects.all():
        resp_dict[j] = {'id': i.id, 'sex': i.sex}
        j += 1

    return JsonResponse(resp_dict, safe=False)


def api_source_org_list(request: HttpRequest):
    resp_dict = {}
    j = 0
    for i in source_org.objects.all():
        resp_dict[j] = {"id": i.id, "name": i.name}
        j += 1

    return JsonResponse(resp_dict, safe=False)


def api_original_information_list(request: HttpRequest):
    resp_dict = {}
    j = 0
    for i in original_information.objects.all():
        resp_dict[j] = {"id": i.id, "ecg_id": i.ecg_id.id}
        j += 1

    return JsonResponse(resp_dict, safe=False)


def api_access_groups_list(request: HttpRequest):
    resp_dict = {}
    j = 0
    for i in access_groups.objects.all():
        resp_dict[j] = {"id": i.id, "name": i.name,
                        'description': i.description}
        j += 1

    return JsonResponse(resp_dict, safe=False)


def view_file(request: HttpRequest, id: int):
    file_obj = get_object_or_404(ecg_files, id=id)
    return render(
        request,
        'view_pages/file_view.html',
        context={'o_file': file_obj, 'page_title': 'Информация о файле'},
    )


def api_file_info(request: HttpRequest, id: int):
    file_obj = get_object_or_404(ecg_files, id=id)
    return JsonResponse({'ecg_id': file_obj.ecg_id.id,
                         'format': file_obj.format,
                         'file_hash': file_obj.file_hash,
                         'sample_frequency': file_obj.sample_frequency,
                         'amplitude_resolution': file_obj.amplitude_resolution,
                         'original_name': file_obj.original_name})


def file_download_link(request: HttpRequest, id: int):
    file_obj = get_object_or_404(ecg_files, id=id)
    # добавить проверку на доступ к файлу
    return redirect(file_obj.get_minio_download_link(link_live_duration=timedelta(minutes=5)))


def view_patient(request: HttpRequest, id: int):
    patient = get_object_or_404(patients, id=id)
    form = PatientForm(instance=patient)
    return render(
        request,
        'view_pages/patient_view.html',
        context={'form': form, 'page_title': 'Информация о пациенте'},
    )


def api_patient_info(request: HttpRequest, id: int):
    patient = get_object_or_404(patients, id=id)
    return JsonResponse({"sex": patient.sex,
                         "birthdate": patient.birthdate,
                         "name": patient.name,
                         "last_name": patient.last_name,
                         "middle_name": patient.middle_name})


def view_ecg(request: HttpRequest, id: int):
    ecg_inst = get_object_or_404(ecg, id=id)
    form = EcgForm(instance=ecg_inst)
    return render(
        request,
        'view_pages/ecg_view.html',
        context={'form': form, 'page_title': 'Информация о экг'},
    )


def api_ecg_info(request: HttpRequest, id: int):
    ecg_inst = get_object_or_404(ecg, id=id)
    return JsonResponse({'check_date': ecg_inst.check_date,
                         'add_date': ecg_inst.add_date,
                         'patient_age': ecg_inst.patient_age,
                         'patient_id': get_ForeginKey_id_or_empty(ecg_inst.patient_id),
                         'source_user': get_ForeginKey_id_or_empty(ecg_inst.source_user),
                         'access_id': get_ForeginKey_id_or_empty(ecg_inst.access_id),
                         'org_id': get_ForeginKey_id_or_empty(ecg_inst.org_id)})


def api_source_org_info(request: HttpRequest, id: int):
    org_inst = get_object_or_404(source_org, id=id)
    return JsonResponse({"name": org_inst.name,
                         "description": org_inst.description})


def api_original_information_info(request: HttpRequest, id: int):
    inf_inst = get_object_or_404(original_information, id=id)
    return JsonResponse({"ecg_id": inf_inst.ecg_id.id,
                         "idMedServ": inf_inst.idMedServ,
                         "patientId": inf_inst.patientId,
                         "result": inf_inst.result})


@login_required
def edit_patient(request: HttpRequest, id: int):
    patient = get_object_or_404(patients, id=id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect(patient.get_absolute_url())
    else:
        form = PatientForm(instance=patient)

    return render(request,
                  'post_forms/common_form.html',
                  context={'form': form, 'page_title': 'Редактирование пациента'},)


@csrf_exempt
@login_required
def api_edit_patient(request: HttpRequest, id: int):
    patient = get_object_or_404(patients, id=id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse(form.errors, status=400, safe=False)
    return HttpResponseBadRequest()


@login_required
def edit_file(request: HttpRequest, id: int):
    file_obj = get_object_or_404(ecg_files, id=id)
    if request.method == 'POST':
        form = FileEditForm(request.POST, instance=file_obj)
        if form.is_valid():
            r = form.save()
            return redirect(file_obj.get_absolute_url())
    else:
        form = FileEditForm(instance=file_obj)

    return render(
        request,
        'post_forms/file_edit.html',
        context={'form': form,
                 'page_title': 'Редактирование записи ecg файла'},
    )


@csrf_exempt
@login_required
def api_edit_ecg_file(request: HttpRequest, id: int):
    file_obj = get_object_or_404(ecg_files, id=id)
    if request.method == 'POST':
        form = FileEditForm(request.POST, instance=file_obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse(form.errors, status=400, safe=False)
    return HttpResponseBadRequest()


@login_required
def edit_ecg(request: HttpRequest, id: int):
    ecg_inst = get_object_or_404(ecg, id=id)
    if request.method == 'POST':
        form = EcgForm(request.POST, instance=ecg_inst)
        if form.is_valid():
            form.save()
            return redirect(ecg_inst.get_absolute_url())
    else:
        form = EcgForm(instance=ecg_inst)

    return render(request,
                  'post_forms/common_form.html',
                  context={'form': form, 'page_title': 'Редактирование ЭКГ'},)


@csrf_exempt
@login_required
def api_edit_ecg(request: HttpRequest, id: int):
    ecg_inst = get_object_or_404(ecg, id=id)
    if request.method == 'POST':
        form = EcgForm(request.POST, instance=ecg_inst)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse(form.errors, status=400, safe=False)
    return HttpResponseBadRequest()


@csrf_exempt
@login_required
def api_edit_original_information(request: HttpRequest, id: int):
    or_inf = get_object_or_404(original_information, id=id)
    if request.method == 'POST':
        form = OriginalInformation(request.POST, instance=or_inf)
        if form.is_valid():
            result = form.save()
            return JsonResponse({'success': True})
        else:
            JsonResponse(form.errors, status=400, safe=False)
    return HttpResponseBadRequest()


@login_required
def add_ecg_file(request: HttpRequest):
    ecg_id = request.GET.get('ecg_id', '')
    sample_frequency = request.GET.get('sample_frequency', '')
    amplitude_resolution = request.GET.get('amplitude_resolution', '')
    form = FileUploadForm(initial={'ecg_id_field': ecg_id, 'sample_frequency_field': sample_frequency,
                                   'amplitude_resolution_field': amplitude_resolution})
    return render(
        request,
        'post_forms/upload_file.html',
        context={'form': form, 'page_title': 'Добаление ecg файла'},
    )


@csrf_exempt
@login_required
def api_add_ecg_file(request: HttpRequest):
    if request.method == 'POST':
        form = FileUploadForm(request.POST)
        if form.is_valid():
            dict_response = {}
            new_ecg_file = form.save()
            dict_response['upload_url'] = new_ecg_file.get_minio_upload_link(
                link_live_duration=timedelta(minutes=5))
            dict_response['ecg_file_id'] = new_ecg_file.id
            dict_response['redirect_url'] = new_ecg_file.get_absolute_url()
            return JsonResponse(dict_response)
        else:
            data = form.errors
            return JsonResponse(data, status=400, safe=False)
    return HttpResponseBadRequest()


@login_required
def add_patient(request: HttpRequest):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            result = form.save()
            return redirect(result.get_absolute_url())
    else:
        form = PatientForm()

    return render(request,
                  'post_forms/common_form.html',
                  context={'form': form, 'page_title': 'Добавление пациента'},)


@csrf_exempt
@login_required
def api_add_patient(request: HttpRequest):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            result = form.save()
            return JsonResponse({'id': result.id})
        else:
            JsonResponse(form.errors, status=400, safe=False)
    return HttpResponseBadRequest()


@login_required
def add_ecg(request: HttpRequest):
    if request.method == 'POST':
        form = EcgForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.source_user = request.user
            result.save()
            return redirect(result.get_absolute_url())
    else:
        group = access_groups.objects.filter(name='Default')[0]
        form = EcgForm(
            initial={'source_user': request.user, 'access_id': group})

    return render(request,
                  'post_forms/common_form.html',
                  context={'form': form, 'page_title': 'Добавление ЭКГ'},)


@csrf_exempt
@login_required
def api_add_ecg(request: HttpRequest):
    if request.method == 'POST':
        form = EcgForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.source_user = request.user
            result.save()
            dict_response = {}
            dict_response["id"] = result.id
            return JsonResponse(dict_response)
        else:
            JsonResponse(form.errors, status=400, safe=False)
    return HttpResponseBadRequest()


@csrf_exempt
@login_required
def api_add_original_information(request: HttpRequest):
    if request.method == 'POST':
        form = OriginalInformation(request.POST)
        if form.is_valid():
            result = form.save()
            return JsonResponse({'id': result.id})
        else:
            JsonResponse(form.errors, status=400, safe=False)
    return HttpResponseBadRequest()


@csrf_exempt
def api_login(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    data = {'success': True}
                else:
                    data = {'success': False, 'error': 'User is not active'}
            else:
                data = {'success': False,
                        'error': 'Wrong username and/or password'}
        return JsonResponse(data)
    return HttpResponseBadRequest()
