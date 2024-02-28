from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ItemSerializer
from .models import Item
import uuid

# Model(Item): id name description tags price user_id

@api_view(['GET'])
@permission_classes([AllowAny])
def GetAllItems(request):
    count = request.GET.get('count', 20)
    # Sanitize params
    try:
        count = int(count)
    except ValueError:
        return JsonResponse({'error': 'Invalid count parameter, must be an integer'}, status=400)
    
    if count < 1 or count > 30:
        return JsonResponse({'error': 'Count parameter too large'}, status=400)
    
    all_items = Item.objects.all()[:count]
    serializer = ItemSerializer(all_items, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def GetItem(request, item_id):
    try:
        item = Item.objects.get(id = item_id)
        serializer = ItemSerializer(item)
        return JsonResponse(serializer.data, status=200)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

@api_view(['GET'])
def GetAllUserItems(request):
    # TODO: verify Seller qualification
    user_id = request.data.get('user_id')
    user_items = Item.objects.filter(user_id = user_id)
    if user_items.exists():
        serializer = ItemSerializer(user_items, many=True)
        return JsonResponse(serializer.data, status=200)
    else:
        return JsonResponse({}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def CreateItem(request):
    # TODO: verify User login status
    req_data = request.data
    saved = False
    while not saved:
        req_data['id'] = uuid.uuid4()
        serializer = ItemSerializer(data=req_data)
        if serializer.is_valid():
            try:
                serializer.save()
                saved = True
                return JsonResponse(serializer.data, status=201)
            except IntegrityError:
                continue
        else:
            return JsonResponse(serializer.errors, status=400)
    
@api_view(['PATCH'])
def UpdateItem(request, item_id):
    try:
        # TODO: verify Seller qualification
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
    serializer = ItemSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=400)
    
@api_view(['DELETE'])
@permission_classes([AllowAny])
def DeleteItem(request, item_id):
    try:
        # TODO: verify Seller qualification
        item = Item.objects.get(id=item_id)
        item.delete()
        return JsonResponse({'message': 'Item deleted'}, status=200)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
