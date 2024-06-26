# Generated by Django 3.1.6 on 2021-02-19 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecg_storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='access_groups',
            options={'ordering': ['-name']},
        ),
        migrations.AddField(
            model_name='access_groups',
            name='name',
            field=models.CharField(default=1, help_text='Название группы', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
