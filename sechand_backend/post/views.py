from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import ItemSerializer
from .models import Item

# Model(Item): id name description tags price user_id

@api_view(['GET'])
def GetAllItems(request):
    all_items = Item.objects.all()
    serializer = ItemSerializer(all_items, many=True)

    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['GET'])
def GetSingleItem(request, item_id):
    try:
        item = Item.objects.get(id = item_id)
        serializer = ItemSerializer(item)
        return JsonResponse(serializer.data, status=200)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

@api_view(['POST'])
def CreateItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    else:
        return JsonResponse(serializer.errors, status=404)
    
@api_view(['PATCH'])
def UpdateItem(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
    serializer = ItemSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    else:
        return JsonResponse(serializer.errors, status=400)