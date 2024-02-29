from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import VerifyEmailCode, ResetPasswordCode, Address
from .utils import send_verify_email, send_reset_password
from .serializers import CustomUserSerializer, VerifyEmailCodeSerializer, ResetPasswordCodeSerializer


UserModel = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(username, password)
    try:
        user = UserModel.objects.get(username=username)
        if user.check_password(password):
            if user.is_verified:
                login(request, user)
                serializer = CustomUserSerializer(user)
                # registered, correct password
                return JsonResponse({'registered': True, 'success': True, 'userInfo': serializer.data})
            else:
                # User is not active, prompt for email verification
                user.delete()
                # registered, not verified
                return JsonResponse({'registered': True, 'success': False, 'userInfo': None})
        else:
            # registered, incorrect password
            return JsonResponse({'registered': True, 'success': False, 'userInfo': None})
    except UserModel.DoesNotExist:
        # 3.2. not registered
        return JsonResponse({'registered': False, 'success': False, 'userInfo': None})
    
    # 1. registered, correct password
    # 2. registered, incorrect password
    # 3. not registered
    #   3.1. registered, not verified
    #   3.2. not registered


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    phone = request.data.get('phone')
    displayname = request.data.get('displayname')
    address_id = request.data.get('address')
    address = Address.objects.get(id=address_id)
    image = request.data.get('image')
    is_visible = request.data.get('is_visible')
    print(username, password, email)
    try:
        user = UserModel.objects.get(username=username)
        if not user.is_verified:
            # Update the user
            user.username = username
            user.set_password(password)
            user.email = email
            user.phone = phone
            user.displayname = displayname
            user.address = address
            user.image = image
            user.is_visible = is_visible
            user.save()
            # Send verification email with the code
            try:
                send_verify_email(user)
                serializer = CustomUserSerializer(user)
                # registered, not verified
                return JsonResponse({"new_user": True, "user": serializer.data})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            # registered and verified
            return JsonResponse({"new_user": False, "user": None})
    except UserModel.DoesNotExist:
        # Create the user
        user = UserModel.objects.create_user(username=username, email=email, password=password, phone=phone,
                                             displayname=displayname, address=address, image=image, is_visible=is_visible)
        # Send verification email with the code
        try:
            send_verify_email(user)
            serializer = CustomUserSerializer(user)
            # not registered, not verified
            return JsonResponse({"new_user": True, "user": serializer.data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request, uid):
    # user = request.user
    code = request.data.get('code')
    try:
        user = UserModel.objects.get(pk=uid)
        if not user.is_verified:
            try:
                verification_code = VerifyEmailCode.objects.get(user=user)
                if verification_code.code != code:
                    # code is incorrect
                    return JsonResponse({'expired': False, 'correct': False})
                if verification_code.is_expired():
                    # code has expired
                    return JsonResponse({'expired': True, 'correct': True})
                # Update the user's status to verified
                user.is_verified = True
                user.save()
                verification_code.delete()
                # code is verified
                return JsonResponse({'expired': False, 'correct': True})
            except VerifyEmailCode.DoesNotExist:
                # code has never been sent
                return JsonResponse({'message': 'Invalid verification code.'}, status=404)
        else:
            # email has been verified
            return JsonResponse({'message': 'Email already verified.'}, status=400)
    except UserModel.DoesNotExist:
        # user does not exist
        return JsonResponse({'message': 'Invalid user.'}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    try:
        user = UserModel.objects.get(email=email)
        try:
            if user.is_verified:
                send_reset_password(user)
                # success
                return JsonResponse({"registered": True, "sent": True, "uid": user.id})
            else:
                # user registered, not verified
                return JsonResponse({"registered": False, "sent": False})
        except Exception as e:
            return JsonResponse({"registered": False, "sent": False}, status=400)
    except UserModel.DoesNotExist:
        # emial not registered
        return JsonResponse({"registered": False, "sent": False})


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def verify_code(request, uid):
#     code = request.data.get('code')
#     try:
#         code = request.data.get('code')
#         # uid = force_str(urlsafe_base64_decode(uidb64))
#         user = UserModel.objects.get(pk=uid)
#         try:
#             verification_code = ResetPasswordCode.objects.get(user=user)
#             if verification_code.code != code:
#                 return JsonResponse({'message': 'Invalid verification code.'}, status=400)
#             if verification_code.is_expired():
#                 return JsonResponse({'message': 'The verification code has expired.'}, status=400)
#             serializer = ResetPasswordCodeSerializer(verification_code)
#             return JsonResponse(serializer.data, status=201)
#         except ResetPasswordCode.DoesNotExist:
#             return JsonResponse({'message': 'Invalid verification code.'}, status=404)
#     except ResetPasswordCode.DoesNotExist or UserModel.DoesNotExist:
#         return JsonResponse({'message': 'Invalid verification code.'}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, jhed):
    code = request.data.get('code')
    try:
        # Update the user's password
        user = UserModel.objects.get(username=jhed)
        verification_code = ResetPasswordCode.objects.get(user=user)
        if verification_code.code != code:
            return JsonResponse({'expired': False, 'correct': False})
        if verification_code.is_expired():
            return JsonResponse({'expired': True, 'correct': True})
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        verification_code.delete()
        # password updated
        return JsonResponse({'expired': False, 'correct': True})
    except UserModel.DoesNotExist:
        # new user
        return JsonResponse({'message': 'Invalid user.'}, status=404)


@api_view(['GET'])
def get_user_profile(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return JsonResponse(serializer.data, status=200)


@api_view(['PATCH'])
def update_user_profile(request):
    user = request.user
    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=400)