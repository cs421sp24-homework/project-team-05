from django.db import models

# Create your models here.
class Msg(models.Model):
    context = models.CharField(max_length=3, unique=True)
    content = models.CharField(max_length=60)