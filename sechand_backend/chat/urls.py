from django.urls import path
from . import views

urlpatterns = [
    # POST
    path("Conversation/new", views.CreateRoom, name="CreateRoom"),
]