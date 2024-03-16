import uuid
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    # TODO: shrink below length limit
    category = models.CharField(max_length=128, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)

class UserCollection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.UUIDField()