from django.db import migrations, models


def add_Default_group(apps, schema_editor):
    groups = apps.get_model('ecg_storage', "access_groups")
    if groups.objects.filter(name='Default').count() == 0:
        groups.objects.create(
            name="Default", description="Группа для экг по умолчанию")


class Migration(migrations.Migration):

    dependencies = [
        ('ecg_storage', '0007_auto_20210313_0029'),
    ]

    operations = [
        migrations.RunPython(add_Default_group),
    ]
