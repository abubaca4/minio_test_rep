from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core import validators

from django import forms

from .models import ecg
from .models import ecg_files

class FileUpload(forms.Form):
    ecg_id_field = forms.IntegerField(label='ID экг для которого загружается файл')
    sample_frequency_field = forms.IntegerField(label='Sample frequency')
    amplitude_resolution_field = forms.IntegerField(label='Amplitude resolution')
    file_hash = forms.CharField(validators=[validators.MaxLengthValidator(40), validators.MinLengthValidator(40)])
    file_format = forms.CharField(validators=[validators.MaxLengthValidator(20), validators.MinLengthValidator(1)])

    def clean_ecg_id_field(self):
        data = self.cleaned_data['ecg_id_field']

        if ecg.objects.filter(id=int(data)).count() == 0:
            raise ValidationError(_('Экг с таким ID не существует'))

        return data

    def clean_file_hash(self):
        data = self.cleaned_data['file_hash']

        if ecg_files.objects.filter(file_hash=data).count() != 0:
            raise ValidationError(_('Такой файл уже существует'))

        return data

        
