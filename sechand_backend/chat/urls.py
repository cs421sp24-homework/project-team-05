from django.urls import path
from . import views

urlpatterns = [
    # POST
    # path("Conversation/new", views.CreateRoom, name="CreateRoom"),
    path("Conversation/get/<int:receiver_id>", views.GetRoom, name="GetRoom"),
    path("Conversation/list", views.GetChatList, name="GetChatList"),
    path("Conversation/list/<int:receiver_id>", views.GetChatListWithReceiver, name="GetChatListWithReceiver"),
    path("Conversation/auto-send/<int:receiver_id>/<uuid:item_id>", views.SendItemLink, name="SendItemLink"),
    path("Conversation/message/new", views.NewMessageNotification, name="NewMessageNotification"),
    path("Conversation/message/read", views.ReadMessageNotification, name="ReadMessageNotification"),
    path("Conversation/notification/one-count/<uuid:room_id>", views.GetOneNotificationCount, name="GetOneNotificationCount"),
    path("Conversation/notification/total-count", views.GetTotalNotificationCount, name="GetTotalNotificationCount"),
    path("Conversation/notification/activate", views.ActivateNotification, name="ActivateNotification"),
]