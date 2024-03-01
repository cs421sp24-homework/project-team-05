from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-email/<uid>', views.verify_email, name='verify-email'),
    path('login/', views.custom_login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    # path('verify-code/<uid>', views.verify_code, name='verify-code'),
    path('reset-password/<jhed>', views.reset_password, name='reset-password'),
    path('profile/', views.get_user_profile, name='get-user-profile'),
    path('profile/update', views.update_user_profile, name='update-user-profile'),
    path('init-info/', views.init_info, name='init-info'),
    path('logout/', LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)