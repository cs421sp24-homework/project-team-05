import uuid
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    # TODO: shrink below length limit
    catagory = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)
