"""minio_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static  # заменить на отдачу статики другим способом
from django.conf import settings  # заменить на отдачу статики другим способом
from django.views.generic import RedirectView
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('file_minio_storage/', include('file_minio_storage.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/file_minio_storage/', permanent=True)),
]

# заменить на отдачу статики другим способом
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]