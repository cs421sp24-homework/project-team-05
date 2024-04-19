# Generated by Django 5.0.1 on 2024-04-10 16:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_notification'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together={('user', 'room')},
        ),
    ]