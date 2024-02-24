from django.contrib import admin
from .models import CustomUser, VerifyEmailCode, ResetPasswordCode

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(VerifyEmailCode)
admin.site.register(ResetPasswordCode)