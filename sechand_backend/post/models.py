import uuid
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

# Create your models here.
class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    tags = ArrayField(models.CharField(max_length=200), default=list)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
