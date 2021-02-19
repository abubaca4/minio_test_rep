from django.contrib import admin
from .models import source_org, patients, cardiac_pathology, access_groups, user_access, ecg, ecg_files, original_information, ecg_tasks, ecg_conclusion, conclusion_pathology

# Register your models here.

admin.site.register(source_org)
admin.site.register(patients)
admin.site.register(cardiac_pathology)
admin.site.register(access_groups)
admin.site.register(user_access)
admin.site.register(ecg)
admin.site.register(ecg_files)
admin.site.register(original_information)
admin.site.register(ecg_tasks)
admin.site.register(ecg_conclusion)
admin.site.register(conclusion_pathology)