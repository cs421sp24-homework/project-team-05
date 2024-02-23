from django.urls import path
from . import views

urlpatterns = [
    #ex: /post/all
    path("allItems/view", views.GetAllItems, name="GetAllItems"),
    #ex: /post/singleItem/view/asd341213sdwqa
    path("singleItem/view/<uuid:item_id>", views.GetSingleItem, name="GetSingleItem"),
    #ex: /post/singleItem/create/aavcssd213
    path("singleItem/create", views.CreateItem, name="CreateItem"),
    #ex: /post/singleItem/update/aavcssd213
    path("singleItem/update/<uuid:item_id>", views.UpdateItem, name="UpdateItem")
]