from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ItemSerializer, ItemSerializerWithSellerName, CollectionSerializer
from .serializers import TransactionSerializer, TransactionDeserializer
from .models import Item, UserCollection, Transaction
from user.models import Address
from .utils import get_distance
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
import uuid

# Model(Item): id name description tags price user_id

@api_view(['GET'])
def GetAllUserItems(request):
    if(request.user):
        #TODO: validate user token again
        user_items_list = list(Item.objects.filter(seller = request.user.id))
        user_items = user_items_list[::-1]
        serializer = ItemSerializer(user_items, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    else:
        return JsonResponse({'error': 'User did not login or have valid credentials'}, status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def GetAllItems(request):
    # get user status
    count = request.data.get('count', 20)
    # Sanitize params
    try:
        count = int(count)
    except ValueError:
        print("Invalid count parameter, must be an integer")
        return JsonResponse({'error': 'Invalid count parameter, must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
    
    if count < 1 or count > 30:
        return JsonResponse({'error': 'Count parameter too large'}, status=status.HTTP_400_BAD_REQUEST)
    
    all_items = Item.objects.filter(is_sold=False)[:count]
    serializer = ItemSerializerWithSellerName(all_items, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['GET'])
def GetAllItemsByDistance(request):
    # get user status
    count = request.data.get('count', 20)
    # Sanitize params
    try:
        count = int(count)
    except ValueError:
        print("Invalid count parameter, must be an integer")
        return JsonResponse({'error': 'Invalid count parameter, must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
    
    if count < 1 or count > 30:
        return JsonResponse({'error': 'Count parameter too large'}, status=status.HTTP_400_BAD_REQUEST)
    
    all_items = Item.objects.filter(is_sold=False).exclude(seller=request.user)[:count]
    all_distances = {}
    for item in all_items:
        all_distances[item.id] = get_distance(request.user.address, item.seller.address)
    sorted_items = sorted(list(all_items), key=lambda item: all_distances.get(item.id))
    # for item in sorted_items:
    #     print(all_distances.get(item.id))
    serializer = ItemSerializerWithSellerName(sorted_items, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def AddNewCollection(request,item_id):
    if(request.user):
        #TODO: validate user token again
        collection_data = {"user": request.user.id, "item": item_id}
        serializer = CollectionSerializer(data=collection_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse({'error': 'Failed with serializing new object.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'User did not login or have valid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
# @permission_classes([AllowAny])
def GetUserCollection(request):
    if(request.user):
        #TODO: validate user token again
        try:
            user_id = request.user.id
            collections = UserCollection.objects.filter(user = user_id)
            item_ids =[collection.item for collection in collections]
            items_list = list(Item.objects.filter(id__in=item_ids))
            items = items_list[::-1]
            serializer = ItemSerializerWithSellerName(items, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({},status=status.HTTP_200_OK)
    else:
       return JsonResponse({'error': 'User need to login to browse their collection'}, status.HTTP_401_UNAUTHORIZED) 

@api_view(['DELETE'])
# @permission_classes([AllowAny])
def DeleteUserCollection(request,item_id):
    #TODO: validate user token again
    user_id = request.user.id
    # user_id = request.data['user_id']
    try:
        item = UserCollection.objects.get(user = user_id, item=item_id)
        item.delete()
        return JsonResponse({'message': 'UserCollection deleted'}, status=status.HTTP_200_OK)
    except UserCollection.DoesNotExist:
        return JsonResponse({'error': 'UserCollection not found'}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
# @permission_classes([AllowAny])
def IsUserCollected(request, item_id):
    #TODO: validate user token again
    user_id = request.user.id
    # user_id = request.data['user_id']      # enable this disable above for postman
    try:
        UserCollection.objects.get(user = user_id, item=item_id)
        return JsonResponse({'collected': True}, status=status.HTTP_200_OK)
    except UserCollection.DoesNotExist:
        return JsonResponse({'collected': False}, status=status.HTTP_200_OK)

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
# @permission_classes([AllowAny])
def CreateNewItem(request):
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
    
@api_view(['POST'])
@permission_classes([AllowAny])
def SearchItems(request):
    desc_text = request.POST.get('desc_text', '')
    lowest_price = float(request.POST.get('lowest_price', -1))
    highest_price = float(request.POST.get('highest_price', -1))
    category = request.data['category']
    location = request.POST.getlist('location')  # location could be list
    distance = float(request.POST.get('distance', -1))  # should be in miles  

    print("Search items based on desc: ", desc_text, ",low price: ", lowest_price, ", high price: ", highest_price, ", catgory: ", category)
    print("location: ", location, ", distance: ", distance)
    query = Q()
    items = Item.objects.annotate(
        search=SearchVector('name', 'description')
    )

    if desc_text:
        # query &= (Q(name__icontains=desc_text) | Q(description__icontains=desc_text))
        items = items.filter(search=desc_text)
    
    if lowest_price >= 0:
        # print("filter", lowest_price)
        query &= Q(price__gte=lowest_price)
    
    if highest_price >= 0:
        query &= Q(price__lte=highest_price)
    
    if category != 'all':
        query &= Q(category__exact=category)
    
    if location:
        query &= Q(seller__address__name__in=location)
    
    if distance >= 0:
        user_addr = request.user.address
        all_addresses = Address.objects.all()
        addrLst = [addr for addr in all_addresses if get_distance(user_addr, addr) <= distance]
        print(addrLst)
        # for address in all_addresses:
        #     if get_distance(user_address, address) <= distance:
        #         addrLst.append(address)
        query &= Q(seller__address__in=addrLst)

    # Execute the query
    results = items.filter(query)
    serializer = ItemSerializerWithSellerName(results, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def BrowseOneKindItems(request):
    category_value = request.POST.get('category', '')
    if(category_value == ''):
        # Empty cateogry but accessed this API, consider 404 or 400 bad request.
        return JsonResponse({'error': 'Failed as no category data passed.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if(category_value == 'all'):
        # Return all items
        all_items = Item.objects.all()
        serializer = ItemSerializerWithSellerName(all_items, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    items = Item.objects.filter(category=category_value)
    serializer = ItemSerializerWithSellerName(items, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['POST'])
# @permission_classes([AllowAny])
def SaveTransaction(request):
    print("transaction data", request.data)
    saved = False
    while not saved:
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                saved = True
                # return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                continue
        else:
            return JsonResponse({'error': 'Failed when saving transaction, serializing object.'}, status=status.HTTP_400_BAD_REQUEST)
    
    item_id = request.data['item_id']
    item = Item.objects.get(id=item_id)
    itemSerializer = ItemSerializer(item, data={"is_sold": True}, partial=True)
    if itemSerializer.is_valid():
        itemSerializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(itemSerializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
# @permission_classes([AllowAny])
def GetAllTransactions(request):
    try:
        user_id = request.user.id
        # user_id = request.data['user_id']
        transactions_list = list(Transaction.objects.filter(buyer_id = user_id))
        transactions = transactions_list[::-1]
        serializer = TransactionDeserializer(transactions, many=True)
        print("Ops")
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error saving message: {e}")
        return JsonResponse({"error": e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)