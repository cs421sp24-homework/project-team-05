from django.contrib import admin
from .models import CustomUser, VerifyEmailCode, ResetPasswordCode, Address


admin.site.register(CustomUser)
admin.site.register(VerifyEmailCode)
admin.site.register(ResetPasswordCode)
admin.site.register(Address)