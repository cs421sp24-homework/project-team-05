import uuid
import boto3
import unicodedata
import re
import os
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_image_size(image):
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Image file too large ( > 5MB )")

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
    timestamp = now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{timestamp}_{uuid.uuid4()}.{ext}"
    return f'media/itemImage/{unique_filename}'

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to=gen_unique_filename, blank=True, null=True) #, validators=[validate_image_size]
    # TODO: shrink below length limit
    category = models.CharField(max_length=128, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            # print(self.pk)
            try:
                old_instance = Item.objects.get(pk=self.pk)
                if old_instance.image and self.image and old_instance.image != self.image:
                    self.delete_s3_image(old_instance.image)
            except Item.DoesNotExist:
                pass
        super(Item, self).save(*args, **kwargs)
    
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

class UserCollection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.UUIDField()

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_id = models.UUIDField()
    seller_id = models.BigIntegerField()
    buyer_id = models.BigIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    review = models.TextField(null=True, blank=True, default=None)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0) 
