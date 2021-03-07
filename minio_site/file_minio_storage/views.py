from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

from .models import File_uploaded

from django.http import HttpResponse

from django.utils import timezone

from minio import Minio


def index(request):
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    return render(request,
                  'index.html',
                  context={'num_files': File_uploaded.objects.count(), 'num_visits':num_visits},
                  )


def upload(request):
    return render(request,
                  'file_upload.html',
                  context={},
                  )


def all_files(request):
    client = Minio(
        "172.23.0.7:32768",
        access_key="FAO5WMCSNYII9GNHMEVV6KX4",
        secret_key="rU7dkiJh4XN3dEoXeI9E2wdnIIUdZS9JuyFhG3F7r2UicIVU",
        secure=False,
    )
    list_files = []
    for i in File_uploaded.objects.all():
        list_files += [[i.file_name, i.storage_file_name, client.presigned_get_object(
            "test",
            i.storage_file_name,), i.pub_date]]

    return render(request,
                  'all_files.html',
                  context={'file_list': list_files},
                  )


def get_upload_link(request):
    file_name = request.GET.get('file_name')  # Дополнительные параметры
    visible_name = request.GET.get('visible_name')
    if visible_name is None:
        visible_name = ''
    if (File_uploaded.objects.filter(storage_file_name=file_name).count() == 0):
        File = File_uploaded(file_name=visible_name,
                             storage_file_name=file_name, pub_date=timezone.localtime())
        File.save()
        client = Minio(
            "localhost:32768",
            access_key="FAO5WMCSNYII9GNHMEVV6KX4",
            secret_key="rU7dkiJh4XN3dEoXeI9E2wdnIIUdZS9JuyFhG3F7r2UicIVU",
            secure=False,
        )
        url = client.presigned_put_object("test", file_name)
        return HttpResponse(url)
    else:
        return HttpResponse(status=409)
