from django.db import models

# Create your models here.


class File_uploaded(models.Model):
    file_name = models.CharField(
        max_length=200, default='', blank=True)
    storage_file_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        if self.file_name == '':
            return self.storage_file_name
        else:
            return self.file_name
