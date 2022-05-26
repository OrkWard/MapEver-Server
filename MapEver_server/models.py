from django.db import models

class upload_file(models.Model):
    name = models.CharField(verbose_name='File Name', max_length=100)
    form = models.CharField(max_length=20)
    data = models.FileField(upload_to='')