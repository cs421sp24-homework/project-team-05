from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ItemSerializer, ItemSerializerWithSellerName, CollectionSerializer, CollectionDeserializer
from .models import Item, UserCollection
from django.db.models import Q
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
    print(request.data)
    count = request.data.get('count',20)
    # Sanitize params
    try:
        count = int(count)
        print(count)
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
    # if(request.user):
        #TODO: validate user token again
        user_id = request.data['id']
        collections = UserCollection.objects.filter(user = user_id)
        if collections.exists():
            serializer = CollectionDeserializer(collections, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse({}, status=200)
    # else:
    #    return JsonResponse({'error': 'User need to login to browse their collection'}, status.HTTP_401_UNAUTHORIZED) 

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
            # user_id = request.data['id']
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
    
@api_view(['POST'])
@permission_classes([AllowAny])
def SearchItems(request):
    desc_text = request.GET.get('desc_text', '')
    lowest_price = request.GET.get('lowest_price', '')
    highest_price = request.GET.get('highest_price', '')
    category = request.GET.get('category', '')

    print(desc_text, "low", lowest_price, "high", highest_price, "cat", category)

    query = Q()

    if desc_text:
        query &= (Q(name__icontains=desc_text) | Q(description__icontains=desc_text))
    
    if lowest_price:
        print("filter", lowest_price)
        query &= Q(price__gte=lowest_price)
    
    if highest_price:
        query &= Q(price__lte=highest_price)
    
    if category:
        query &= Q(category__exact=category)

    # Execute the query
    results = Item.objects.filter(query)
    serializer = ItemSerializerWithSellerName(results, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)