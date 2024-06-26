from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core import validators

from django import forms

from .models import ecg
from .models import ecg_files
from .models import patients
from .models import original_information


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = ecg_files
        fields = ['ecg_id', 'format', 'file_hash',
                  'sample_frequency', 'amplitude_resolution', 'original_name']


class FileEditForm(forms.ModelForm):
    class Meta:
        model = ecg_files
        fields = ['ecg_id', 'sample_frequency',
                  'amplitude_resolution', 'original_name']


class PatientForm(forms.ModelForm):
    class Meta:
        model = patients
        fields = ['sex', 'birthdate', 'name', 'last_name', 'middle_name']


class EcgForm(forms.ModelForm):
    class Meta:
        model = ecg
        fields = ['check_date', 'patient_age',
                  'patient_id', 'access_id', 'org_id']

class OriginalInformation(forms.ModelForm):
    class Meta:
        model = original_information
        fields = ['ecg_id', 'idMedServ',
                  'patientId', 'result']
