from django.db import models
from django.utils import timezone
from django.conf import settings #or from my_project import settings
import time

def date_path(instance, filename):
    f = time.strftime('/%Y/%m/%d')
    t = time.strftime('/%s') 
    name = instance.nombre_completo + "_" + filename.replace(" ","_")
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'documents' + f + t + "_"+  name

def sesion_path(instance, filename):
    f = time.strftime('/%Y/%m/%d')
    t = time.strftime('/%s') 
    name = instance.username + "_" + filename.replace(" ","_")
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'documents' + f + t + "_"+  name

class Registro(models.Model):
  ruta = models.CharField(max_length=200)
  nombre_completo = models.CharField(max_length=100)
  docfile = models.FileField(upload_to=date_path)
  username = models.CharField(max_length=20)
  faceId = models.CharField(max_length=50)
  created_date = models.DateTimeField(
          default=timezone.now)
  published_date = models.DateTimeField(
          blank=True, null=True)

  def __str__(self):
    return self.faceId

class Sesion(models.Model):
  ruta = models.CharField(max_length=100)
  username = models.CharField(max_length=20)
  faceId = models.CharField(max_length=50)
  sesion_file = models.FileField(upload_to=sesion_path)
  created_date = models.DateTimeField(
          default=timezone.now)
  published_date = models.DateTimeField(
          blank=True, null=True)

  def __str__(self):
    return self.faceId