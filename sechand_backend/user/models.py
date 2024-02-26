from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime, uuid

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=30, blank=True)
    # image = models.ImageField(upload_to='media/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class VerifyEmailCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    # Code expires after 10 minutes
    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=10)


class ResetPasswordCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    # Code expires after 10 minutes
    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=10)