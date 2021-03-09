from django.shortcuts import render

from .models import ecg

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


def add_ecg_file(request):
    return render(
        request,
        'upload_file.html',
        context={'ecg_list': ecg.objects.all()},
    )
