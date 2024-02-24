from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-email/<uid>', views.verify_email, name='verify-email'),
    path('login/', views.custom_login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('verify-code/<uid>', views.verify_code, name='verify-code'),
    path('reset-password/<uid>/<uuid:token>', views.reset_password, name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout')
]