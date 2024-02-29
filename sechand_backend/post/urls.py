from django.urls import path
from . import views

urlpatterns = [
    # GET 
    path("UserItems/all", views.GetAllUserItems, name="GetAllUserItems"),

    # GET
    path("Items/all", views.GetAllItems, name="GetAllItems"),

    # GET PATCH DELETE
    path("Item/<uuid:item_id>", views.ProcessSingleItem, name="GetSingleItem"),

    # POST
    path("Item/new", views.CreateItem, name="CreateItem")
]