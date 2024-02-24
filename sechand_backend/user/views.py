from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str
from rest_framework.decorators import api_view
from .models import VerifyEmailCode, ResetPasswordCode
from .utils import send_verify_email, send_reset_password
from .serializers import CustomUserSerializer, VerifyEmailCodeSerializer, ResetPasswordCodeSerializer


# Create your views here.
UserModel = get_user_model()

@api_view(['POST'])
def custom_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_verified:
            login(request, user)
            serializer = CustomUserSerializer(user)
            return JsonResponse(serializer.data, status=201)
        else:
            # User is not active, prompt for email verification
            user.delete()
            return JsonResponse({'message': 'Please verify your email before logging in.'}, status=401)
    else:
        return JsonResponse({'message': 'Invalid username or password.'}, status=401)


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    print(username, password, email)
    # Create the user
    try:
        user = UserModel.objects.create_user(username=username, email=email, password=password)
        # Send verification email with the code
        try:
            send_verify_email(user)
            serializer = CustomUserSerializer(user)
            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(['POST'])
def verify_email(request, uid):
    # user = request.user
    code = request.data.get('code')
    try:
        # uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
        verification_code = VerifyEmailCode.objects.get(user=user)
        if verification_code.code != code:
            return JsonResponse({'message': 'Invalid verification code.'}, status=400)
        if verification_code.is_expired():
            return JsonResponse({'message': 'The verification code has expired.'}, status=400)
        # Update the user's status to verified
        user.is_verified = True
        user.save()
        verification_code.delete()
        return JsonResponse({'message': 'Email verified successfully.'})
    except VerifyEmailCode.DoesNotExist:
        return JsonResponse({'message': 'User does not exist.'}, status=404)


@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    try:
        user = UserModel.objects.get(email=email)
        try:
            send_reset_password(user)
            serializer = CustomUserSerializer(user)
            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    except UserModel.DoesNotExist:
        return JsonResponse({'message': 'User email does not exist.'}, status=404)


@api_view(['POST'])
def verify_code(request, uid):
    code = request.data.get('code')
    try:
        code = request.data.get('code')
        # uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
        verification_code = ResetPasswordCode.objects.get(user=user)
        if verification_code.code != code:
            return JsonResponse({'message': 'Invalid verification code.'}, status=400)
        if verification_code.is_expired():
            return JsonResponse({'message': 'The verification code has expired.'}, status=400)
        serializer = ResetPasswordCodeSerializer(verification_code)
        return JsonResponse(serializer.data, status=201)
    except ResetPasswordCode.DoesNotExist or UserModel.DoesNotExist:
        return JsonResponse({'message': 'Invalid verification code.'}, status=404)


@api_view(['POST'])
def reset_password(request, uid, token):
    try:
        # Update the user's password
        user = UserModel.objects.get(pk=uid)
        verification_code = ResetPasswordCode.objects.get(user=user)
        if verification_code.token != token:
            return JsonResponse({'message': 'Invalid token.'}, status=400)
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        verification_code.delete()
        return JsonResponse({'message': 'Password reset successfully.'}, status=201)
    except UserModel.DoesNotExist:
        return JsonResponse({'message': 'Invalid user.'}, status=404)

