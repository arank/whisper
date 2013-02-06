from django.db import models

class sound(models.Model):
    data = models.CharField(max_length= 256000 )
    last_name = models.CharField(max_length=600)
#    file = models.FileField(upload_to='documents/%Y/%m/%d')