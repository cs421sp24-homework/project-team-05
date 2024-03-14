from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<int:user_id>/', consumers.ChatConsumer.as_asgi()),
]