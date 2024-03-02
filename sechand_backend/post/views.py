from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ItemSerializer, ItemSerializerWithSellerName, CollectionSerializer, CollectionDeserializer
from .models import Item, UserPurchase, UserCollection
import uuid

# Model(Item): id name description tags price user_id

@api_view(['GET'])
def GetAllUserItems(request):
    if(request.user):
        #TODO: validate user token again
        user_items = Item.objects.filter(seller = request.user.id)
        if user_items.exists():
            serializer = ItemSerializer(user_items, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse({}, status=200)
    else:
        return JsonResponse({'error': 'User did not login or have valid credentials'}, status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def GetAllItems(request):
    # get user status
    count = request.data.get('count', 4)
    # Sanitize params
    try:
        count = int(count)
    except ValueError:
        return JsonResponse({'error': 'Invalid count parameter, must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
    
    if count < 1 or count > 30:
        return JsonResponse({'error': 'Count parameter too large'}, status=status.HTTP_400_BAD_REQUEST)
    
    all_items = Item.objects.all()[:count]
    serializer = ItemSerializerWithSellerName(all_items, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def AddNewCollection(request):
    if(request.user):
        #TODO: validate user token again
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse({'error': 'Failed with serializing new object.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'User did not login or have valid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def GetUserCollection(request):
    if(request.user):
        #TODO: validate user token again
        # user_id = request.data['id']
        collections = UserCollection.objects.filter(user = request.user.id)
        if collections.exists():
            serializer = CollectionDeserializer(collections, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse({}, status=200)
    else:
       return JsonResponse({'error': 'User need to login to browse their collection'}, status.HTTP_401_UNAUTHORIZED) 

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def ProcessSingleItem(request, item_id):
    if(request.method == "GET"):
        try:
            item = Item.objects.get(id = item_id)
            serializer = ItemSerializerWithSellerName(item)
            return JsonResponse(serializer.data, status=200)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)          
    elif(request.method == "PATCH"):
        if(request.user):
            try:
            #TODO: validate user token again
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                return JsonResponse({'error': 'Item not found'}, status=404)
        else:
            return JsonResponse({'error': 'User did not login or have valid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif(request.method == "DELETE"):
        if(request.user):
            #TODO: validate user token again
            user_id = request.user.id
            try:
                item = Item.objects.get(id=item_id, seller=user_id)
                item.delete()
                return JsonResponse({'message': 'Item deleted'}, status=200)
            except Item.DoesNotExist:
                return JsonResponse({'error': 'Item not found'}, status=404)
        else:
            return JsonResponse({'error': 'User did not login or have valid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['POST'])
# TODO: remove when actural release
@permission_classes([AllowAny])
def CreateNewItem(request):
    if(request.user):
        #TODO: validate user token again
        req_data = request.data
        saved = False
        while not saved:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    saved = True
                    return JsonResponse(serializer.data, status=201)
                except IntegrityError:
                    continue
            else:
                return JsonResponse({'error': 'Failed with serializing new object.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'User did not login or have valid credentials'}, status=status.HTTP_401_UNAUTHORIZED)