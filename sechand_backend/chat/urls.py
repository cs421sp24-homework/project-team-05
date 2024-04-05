from django.urls import path
from . import views

urlpatterns = [
    # POST
    path("Conversation/new", views.CreateRoom, name="CreateRoom"),
    path("Conversation/get", views.GetOrCreateRoom, name="GetOrCreateRoom"),
    path("Conversation/list", views.GetChatList, name="GetChatList"),
    path("Conversation/list/<int:receiver_id>", views.GetChatListWithReceiver, name="GetChatListWithReceiver"),
    path("Conversation/auto-send/<int:receiver_id>/<uuid:item_id>", views.SendItemLink, name="SendItemLink"),
]