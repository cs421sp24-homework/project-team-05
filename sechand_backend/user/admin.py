from django.contrib import admin
from .models import CustomUser, VerifyEmailCode, ResetPasswordCode


admin.site.register(CustomUser)
admin.site.register(VerifyEmailCode)
admin.site.register(ResetPasswordCode)