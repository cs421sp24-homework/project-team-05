from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Room, Message
from post.models import Item
from post.serializers import ItemSerializer
from .serializers import RoomSerializer, RoomSerializerWithMessages
from django.db.models import Q, Exists, OuterRef

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
        
@api_view(['POST'])
@permission_classes([AllowAny])
def CreateRoom(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def GetOrCreateRoom(request):
    user1 = request.user
    user2 = request.data['receiver']
    room = Room.objects.filter(Q(users__contains=[user1.id]) & Q(users__contains=[user2.id]))
    if room.exists():
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        room = Room.objects.create(users=[user1.id, user2.id])
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


@api_view(['POST'])
def SendItemLink(request, receiver_id, item_id):
    item = Item.objects.get(id=item_id)
    try:
        room = Room.objects.get(Q(users__contains=[request.user.id]) & Q(users__contains=[receiver_id]))
    except Room.DoesNotExist:
        room = Room.objects.create(users=[request.user.id, receiver_id])
    message = Message.objects.create(
        room=room,
        sender=request.user,
        data=ItemSerializer(item).data,
        content='Hi, I\'m interested in this item.'
    )
    room_group_name = 'chat_%s' % room.id
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'chat_message',
            'content': message.content,
            'data': message.data,
            'sender': message.sender,
            'timestamp': message.timestamp,
            'room_id': room.id,
        }
    )
    print("auto send link")
    return Response({'message': 'item link sent'}, status=status.HTTP_200_OK)