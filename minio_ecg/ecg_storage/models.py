from django.db import models

# Create your models here.

class source_org(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Название организации")
    description = models.TextField(help_text="Дополнительная информация об организации", null=True, blank = True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name