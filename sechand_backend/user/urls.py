from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-email/<uid>', views.verify_email, name='verify_email'),
    path('login/', views.custom_login, name='custom_login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    # path('verify-code/<uid>', views.verify_code, name='verify-code'),
    path('reset-password/<jhed>', views.reset_password, name='reset_password'),
    path('profile/', views.get_user_profile, name='get_user_profile'),
    path('profile/update', views.update_user_profile, name='update_user_profile'),
    path('init-info/', views.init_info, name='init_info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/order-history', views.get_order_history, name='get_order_history'),
    path('profile/order-history/new', views.add_new_purchase_history, name='add_new_purchase_history')
]