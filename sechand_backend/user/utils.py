from django.core.mail import send_mail
from django.conf import settings
from .models import VerificationCode
import random


def send_verification_email(user):
    # Generate a random six-digit code
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Create or update the verification code for the user
    VerificationCode.objects.update_or_create(user=user, defaults={'code': code})
    
    # Send email
    send_mail(
        'Verify Your Email',
        f'Hi {user.username}, your verification code is: {code}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )