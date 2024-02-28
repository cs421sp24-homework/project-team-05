from django.urls import path
from . import views

urlpatterns = [
    # GET 
    path("User/Items/all", views.GetAllUserItems, name="GetAllUserItems"),

    # GET
    path("Items/all", views.GetAllItems, name="GetAllItems"),

    # GET
    path("Item/<uuid:item_id>", views.GetItem, name="GetSingleItem"),

    # POST
    path("Item/new", views.CreateItem, name="CreateItem"),

    # PATCH
    path("Item/<uuid:item_id>", views.UpdateItem, name="UpdateItem"),

    # DELETE
    path("Item/<uuid:item_id>", views.DeleteItem, name="DeleteItem")
]