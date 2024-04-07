import boto3
import unicodedata
import re
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from post.models import Item
import datetime, uuid

def gen_unique_filename(instance, filename):

    def normalize_name(filename):
        filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
        return filename
    
    def sanitize_name(filename):
        filename = re.sub(r'\W+', '_', filename)
        return filename

    name, ext = os.path.splitext(filename)
    name = normalize_name(name)
    name = sanitize_name(name)
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{timestamp}_{uuid.uuid4()}.{ext}"
    return f'media/userAvatar/{unique_filename}'

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)
    displayname = models.CharField(max_length=30)
    image = models.ImageField(upload_to=gen_unique_filename, blank=True, null=True)
    is_visible = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            print(self.pk)
            try:
                old_instance = CustomUser.objects.get(pk=self.pk)
                if old_instance.image and self.image and old_instance.image != self.image:
                    self.delete_s3_image(old_instance.image)
            except CustomUser.DoesNotExist:
                pass
        super(CustomUser, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.delete_s3_image(self.image)
        super(Item, self).delete(*args, **kwargs)

    def delete_s3_image(self, image):
        s3_resource = boto3.resource(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        bucket = s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        path = image.name
        bucket.Object(path).delete()

    def __str__(self):
        return self.username


class VerifyEmailCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    # Code expires after 1 minute
    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=2)


class ResetPasswordCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    # Code expires after 1 minute
    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=2)
    

class Address(models.Model):
    name = models.CharField(max_length=30, unique=True)
    street = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=5)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name
    
class UserPurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.UUIDField()