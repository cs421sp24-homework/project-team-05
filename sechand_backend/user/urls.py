from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('send-verification-code/', views.send_verification_email, name='send_verification_code'),
    path('verify-email/', views.verify_code, name='verify-email'),
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]