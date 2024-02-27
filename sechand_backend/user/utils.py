from django.core.mail import send_mail
from django.conf import settings
from .models import VerifyEmailCode, ResetPasswordCode
import random, uuid
from django.utils import timezone


def send_verify_email(user):
    # Generate a random six-digit code
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Create or update the verification code for the user
    VerifyEmailCode.objects.update_or_create(user=user, defaults={'code': code, 'created_at': timezone.now()})
    
    # Send email
    send_mail(
        'Sechand Email Verification Code',
        f'Hi {user.username}, please use this code to verify your email address: {code}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

def send_reset_password(user):
    # Generate a random six-digit code
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    token = uuid.uuid4()
    
    # Create or update the verification code for the user
    ResetPasswordCode.objects.update_or_create(user=user, defaults={'code': code, 'token': token, 'created_at': timezone.now()})
    
    # Send email
    send_mail(
        'Sechand Password Reset Code',
        f'Hi {user.username}, please use this code to reset your password: {code}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )