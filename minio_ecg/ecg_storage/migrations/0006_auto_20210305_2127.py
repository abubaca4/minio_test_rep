# Generated by Django 3.1.7 on 2021-03-05 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecg_storage', '0005_auto_20210305_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecg',
            name='check_date',
            field=models.DateField(blank=True, help_text='Дата снятия показаний', null=True),
        ),
    ]
