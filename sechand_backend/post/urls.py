from django.urls import path
from . import views

urlpatterns = [
    path("allItems/view/<uuid:item_id>", views.GetAllUserItems, name="GetAllUserItems"),

    # GET ex: /post/all
    path("allItems/view", views.GetAllItems, name="GetAllItems"),

    # GET ex: /post/singleItem/view/asd341213sdwqa
    path("singleItem/view/<uuid:item_id>", views.GetSingleItem, name="GetSingleItem"),

    # POST ex: /post/singleItem/create/aavcssd213
    path("singleItem/create", views.CreateItem, name="CreateItem"),

    # PATCH ex: /post/singleItem/update/aavcssd213
    path("singleItem/update/<uuid:item_id>", views.UpdateItem, name="UpdateItem"),

    # DELETE ex: /post/singleItem/delete/aavcssd213
    path("singleItem/delete/<uuid:item_id>", views.DeleteItem, name="DeleteItem")
]