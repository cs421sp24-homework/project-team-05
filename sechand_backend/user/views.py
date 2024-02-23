from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import VerificationCode
from .utils import send_verification_email
from .serializers import CustomUserSerializer, VerificationCodeSerializer


# Create your views here.
UserModel = get_user_model()

@api_view(['POST'])
def register(request):
    # Extract registration details from request.POST
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    print(username, password, email)
    # Create the user
    # user = UserModel.objects.create_user(username=username, email=email, password=password, is_active=False)
    try:
        user = UserModel.objects.create_user(username=username, email=email, password=password)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    # Send verification email with the code
    try:
        send_verification_email(user)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    serializer = CustomUserSerializer(user)
    return JsonResponse(serializer.data, status=201)


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
def verify_code(request):
    # user = request.user
    code = request.data.get('code')
    try:
        verification_code = VerificationCode.objects.get(code=code)
        if verification_code.is_expired():
            return JsonResponse({'message': 'The verification code has expired.'}, status=400)
        # Update the user's status to verified
        user = verification_code.user
        user.is_verified = True
        user.save()
        verification_code.delete()
        return JsonResponse({'message': 'Email verified successfully.'})
    except VerificationCode.DoesNotExist:
        return JsonResponse({'message': 'Invalid verification code.'}, status=404)