from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Room, Message, Notification
from post.models import Item
from post.serializers import ItemSerializer
from .serializers import MessageSerializer, RoomSerializer, RoomSerializerWithMessages
from django.db.models import Q, Exists, OuterRef

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@api_view(['GET'])
def GetChatList(request):
    rooms = Room.objects.filter(users__contains=[request.user.id])
    #  retrieve rooms that contain chat history
    rooms_with_messages = rooms.annotate(
            has_message=Exists(Message.objects.filter(room=OuterRef('pk')))
        ).filter(has_message=True)
    serializer = RoomSerializerWithMessages(rooms_with_messages, many=True, context={'request': request})
    sorted_data = sorted(serializer.data, key=lambda x: x['last_message']['timestamp'], reverse=True)
    return Response(sorted_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def GetChatListWithReceiver(request, receiver_id):
    print("receiver_id", receiver_id)
    try:
        prior_room = Room.objects.get(Q(users__contains=[request.user.id]) & Q(users__contains=[receiver_id]))
    except Room.DoesNotExist:
        prior_room = Room.objects.create(users=[request.user.id, receiver_id])
    other_rooms = Room.objects.filter(users__contains=[request.user.id]).exclude(
        users__contains=[receiver_id]).annotate(
            has_message=Exists(Message.objects.filter(room=OuterRef('pk')))
        ).filter(has_message=True)
    # print(prior_room.users)
    serializer_prior = RoomSerializerWithMessages([prior_room], many=True,  context={'request': request})
    # print("serializer_prior", serializer_prior.data)
    serializer_other = RoomSerializerWithMessages(other_rooms, many=True, context={'request': request})
    # print("serializer_other", serializer_other.data)
    sorted_data = sorted(serializer_other.data, key=lambda x: x['last_message']['timestamp'], reverse=True)
    return Response({'chat_list': serializer_prior.data + sorted_data, 'active_chat': 0}, status=status.HTTP_200_OK)


@api_view(['GET'])
def GetRoom(request, receiver_id):
    try:
        Room.objects.get(Q(users__contains=[request.user.id]) & Q(users__contains=[receiver_id]))
        is_new = False
    except Room.DoesNotExist:
        Room.objects.create(users=[request.user.id, receiver_id])
        is_new = True
    return Response(is_new, status=status.HTTP_200_OK)

@api_view(['POST'])
def SendItemLink(request, receiver_id, item_id):
    item = Item.objects.get(id=item_id)
    room = Room.objects.get(Q(users__contains=[request.user.id]) & Q(users__contains=[receiver_id]))
    serialized_room = RoomSerializer(room).data
    
    message = Message.objects.create(
        room=room,
        sender=request.user,
        data=ItemSerializer(item).data,
        content='Hi, I\'m interested in this item.'
    )
    serialized_message = MessageSerializer(message).data

    try:
        notification = Notification.objects.get(user__id=receiver_id, room=room)
    except Notification.DoesNotExist:
        notification = Notification.objects.create(user_id=receiver_id, room=room)
    if notification.active:
        notification.count += 1
        notification.save()
    
    room_group_name = 'chat_%s' % room.id
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'chat_message',
            'content': serialized_message['content'],
            'data': serialized_message['data'],
            'sender': serialized_message['sender'],
            'timestamp': serialized_message['timestamp'],
            'room_id': serialized_room['id'],
        }
    )
    return Response({'message': 'item link sent'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def NewMessageNotification(request):
    room_id = request.data['room_id']
    receiver_id = request.data['receiver_id']
    notification = Notification.objects.get(user__id=receiver_id, room__id=room_id)
    if notification.active:
        notification.count += 1
        notification.save()
    return Response({'message': 'notification sent', 'count': notification.count}, status=status.HTTP_200_OK)


@api_view(['POST'])
def ReadMessageNotification(request):
    room_id = request.data['room_id']
    notification = Notification.objects.get(user=request.user, room__id=room_id)
    notification.count = 0
    notification.active = False
    notification.save()
    return Response({'message': 'notification read', 'count': 0}, status=status.HTTP_200_OK)


@api_view(['GET'])
def GetOneNotificationCount(request, room_id):
    notification = Notification.objects.get(user=request.user, room__id=room_id)
    return Response({'count': notification.count}, status=status.HTTP_200_OK)


@api_view(['GET'])
def GetTotalNotificationCount(request):
    notifications = Notification.objects.filter(user=request.user)
    # print("total notifications", notifications)
    count = sum([notification.count for notification in notifications]) if notifications else 0
    return Response({'count': count}, status=status.HTTP_200_OK)


@api_view(['POST'])
def ActivateNotification(request):
    room_id = request.data['room_id']
    notification = Notification.objects.get(user=request.user, room__id=room_id)
    notification.active=True
    notification.save()
    return Response({'message': 'notification activated'}, status=status.HTTP_200_OK)

    