# Generated by Django 5.0.1 on 2024-02-23 01:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Items',
            new_name='Item',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='ID',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Price',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Tags',
            new_name='tags',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='User_ID',
            new_name='user_id',
        ),
    ]
