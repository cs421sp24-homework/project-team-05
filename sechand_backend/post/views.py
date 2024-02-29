from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import SolelyItemSerializer, ItemSerializerWithSellerName
from .models import Item
import uuid

# Model(Item): id name description tags price user_id

@api_view(['GET'])
def GetAllUserItems(request):
    if(request.user):
        user_id = request.user.id
        user_items = Item.objects.filter(user_id = user_id)
        if user_items.exists():
            serializer = SolelyItemSerializer(user_items, many=True)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({}, status=200)
    else:
        return JsonResponse({'error': 'User did not login or have valid credentials'}, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def GetAllItems(request):
    # get user status
    count = request.data.get('count', 4)
    # Sanitize params
    try:
        count = int(count)
    except ValueError:
        return JsonResponse({'error': 'Invalid count parameter, must be an integer'}, status=400)
    
    if count < 1 or count > 30:
        return JsonResponse({'error': 'Count parameter too large'}, status=400)
    
    all_items = Item.objects.all()[:count]
    serializer = ItemSerializerWithSellerName(all_items, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def ProcessSingleItem(request, item_id):
    if(request.method == "GET"):
        try:
            item = Item.objects.get(id = item_id)
            serializer = SolelyItemSerializer(item)
            return JsonResponse(serializer.data, status=200)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)          
    elif(request.method == "PATCH"):
        if(request.user):
            try:
            # TODO: verify Seller qualification
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                return JsonResponse({'error': 'Item not found'}, status=404)
        else:
            return JsonResponse({'error': 'User did not login or have valid credentials'}, status=400)
        
        serializer = SolelyItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)
    elif(request.method == "DELETE"):
        if(request.user):
            user_id = request.user.id
            try:
                item = Item.objects.get(id=item_id, user_id=user_id)
                item.delete()
                return JsonResponse({'message': 'Item deleted'}, status=200)
            except Item.DoesNotExist:
                return JsonResponse({'error': 'Item not found'}, status=404)
        else:
            return JsonResponse({'error': 'User did not login or have valid credentials'}, status=400)
        
@api_view(['POST'])
# TODO: remove when actural release
@permission_classes([AllowAny])
def CreateNewItem(request):
    if(request.user):
        req_data = request.data
        saved = False
        while not saved:
            req_data['id'] = uuid.uuid4()
            serializer = SolelyItemSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    saved = True
                    return JsonResponse(serializer.data, status=201)
                except IntegrityError:
                    continue
            else:
                return JsonResponse({'error': 'Failed with serializing new object.'}, status=400)
    else:
        return JsonResponse({'error': 'User did not login or have valid credentials'}, status=400)