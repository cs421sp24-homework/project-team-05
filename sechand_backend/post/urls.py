from django.urls import path
from . import views

urlpatterns = [
    path("all", views.GetAllItems, name="GetAllItems")
]