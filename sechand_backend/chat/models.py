from django.db import models
import uuid
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField

# Create your models here.
class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = ArrayField(models.CharField(max_length=200), default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            for user_id in self.users:
                Notification.objects.create(user_id=user_id, room=self)
    
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    data = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='notifications', on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'room')