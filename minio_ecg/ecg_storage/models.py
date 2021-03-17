from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.conf import settings
from django.urls import reverse

from minio import Minio
from datetime import timedelta

# Create your models here.


class source_org(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            help_text="Название организации")
    description = models.TextField(
        help_text="Дополнительная информация об организации", null=True, blank=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return str(self.name)


class patients(models.Model):
    sex_list = [('N', 'Не задан'), ('M', 'Мужской'), ('F', 'Женский')]
    sex = models.CharField(
        max_length=1,
        choices=sex_list,
        default='N',
        help_text="Пол пациента")
    birthdate = models.DateField(
        help_text="Дата рождения", null=True, blank=True)
    name = models.CharField(
        max_length=50, help_text="Имя", null=True, blank=True)
    last_name = models.CharField(
        max_length=50, help_text="Фамилия", null=True, blank=True)
    middle_name = models.CharField(
        max_length=50, help_text="Отчество", null=True, blank=True)

    class Meta:
        ordering = ["-birthdate"]

    def get_absolute_url(self):
        return reverse('patient_view', args=[self.id])

    def get_sex(self):
        for choice in self.sex_list:
            if choice[0] == self.sex:
                return choice[1]
        return ''


class cardiac_pathology(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            help_text="Название патологии")
    short_name = models.CharField(
        max_length=20, help_text="Короткое название", null=True, blank=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return str(self.name)


class access_groups(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            help_text="Название группы")
    description = models.TextField(
        help_text="Информация о группе доступа", null=True, blank=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return str(self.name)


class user_access(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(access_groups, on_delete=models.CASCADE)


class ecg(models.Model):
    check_date = models.DateField(
        help_text="Дата снятия показаний", null=True, blank=True)
    add_date = models.DateTimeField(
        help_text="Дата внесения в систему", auto_now_add=True)
    patient_age = models.IntegerField(help_text="Возраст пациэнта на момент снятия показаний(для показаний не имеющих даты рождения пациента)",
                                      null=True, blank=True, validators=[validators.MinValueValidator(0), validators.MaxValueValidator(150)])
    patient_id = models.ForeignKey(
        patients, models.SET_NULL, blank=True, null=True, help_text="Пациент которому принадлежит экг")
    source_user = models.ForeignKey(
        User, models.SET_NULL, blank=True, null=True, help_text="Пользователь, загрузивший экг на сайт")
    access_id = models.ForeignKey(access_groups, models.SET_NULL, blank=True,
                                  null=True, help_text="Группа доступа к которой принадлежит экг")
    org_id = models.ForeignKey(source_org, models.SET_NULL, blank=True,
                               null=True, help_text="Организация от которой получено экг")

    class Meta:
        ordering = ["-add_date"]

    def __str__(self):
        return str(self.add_date)


class ecg_files(models.Model):
    ecg_id = models.ForeignKey(ecg, on_delete=models.CASCADE)
    format = models.CharField(
        max_length=20, help_text="Тип файла")
    file_hash = models.CharField(
        max_length=40, unique=True, help_text="sha-1 хеш файла")
    sample_frequency = models.IntegerField()
    amplitude_resolution = models.IntegerField()

    def file_name(self) -> str:
        return (self.file_hash + '.' + self.format)

    class Meta:
        ordering = ["-file_hash"]

    def __str__(self):
        return self.file_name()

    def get_minio_download_link(self, link_live_duration: timedelta = None) -> str:
        client = Minio(
            settings.MINIO_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,
        )
        url = None
        if link_live_duration == None:
            url = client.presigned_get_object(
                settings.MINIO_ECG_BUCKET,
                self.file_name())
        else:
            url = client.presigned_get_object(
                settings.MINIO_ECG_BUCKET,
                self.file_name(),
                expires=link_live_duration,
            )
        return url

    def get_minio_upload_link(self, link_live_duration: timedelta = None) -> str:
        client = Minio(
            settings.MINIO_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,
        )
        url = None
        if link_live_duration == None:
            url = client.presigned_put_object(
                settings.MINIO_ECG_BUCKET,
                self.file_name())
        else:
            url = client.presigned_put_object(
                settings.MINIO_ECG_BUCKET,
                self.file_name(),
                expires=link_live_duration,
            )
        return url

    def get_absolute_url(self):
        return reverse('file_view', args=[self.id])


class original_information(models.Model):
    ecg_id = models.ForeignKey(ecg, on_delete=models.CASCADE)
    idMedServ = models.CharField(max_length=20)
    patientId = models.CharField(max_length=20)
    result = models.TextField()


class ecg_tasks(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ecg_id = models.ForeignKey(ecg, on_delete=models.CASCADE)


class ecg_conclusion(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ecg_id = models.ForeignKey(ecg, on_delete=models.CASCADE)
    date_time = models.DateTimeField(
        help_text="Дата вынесения заключения", auto_now_add=True)
    comment = models.TextField(
        help_text="Текстовое заключение", null=True, blank=True)

    class Meta:
        ordering = ["-date_time"]

    def __str__(self):
        return str(self.date_time)


class conclusion_pathology(models.Model):
    conclusion_id = models.ForeignKey(ecg_conclusion, on_delete=models.CASCADE)
    pathology_id = models.ForeignKey(
        cardiac_pathology, on_delete=models.CASCADE)
