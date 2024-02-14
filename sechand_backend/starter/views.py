from django.shortcuts import render
from starter.models import Msg
from django.http import JsonResponse
import json

# Create your views here.
def hello_world(request):
    hw_msg =  Msg.objects.filter(context = 'HLW').first()
    if hw_msg:
        data = {"msg": hw_msg.content}
        return JsonResponse(data)
    else:
        data =  Msg.objects.create(context = 'HLW', content="Hello world!")
        return JsonResponse(data.content)