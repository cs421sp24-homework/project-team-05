from django.urls import path
from . import views

urlpatterns = [
    # GET 
    path("UserItems/all", views.GetAllUserItems, name="GetAllUserItems"),

    # GET
    # request.body parameter:
    #   int count: indicates numbers of each request should return
    path("Items/all", views.GetAllItems, name="GetAllItems"),

    # POST
    path("Item/new", views.CreateNewItem, name="CreateItem"),

    # GET PATCH DELETE
    path("Item/<uuid:item_id>", views.ProcessSingleItem, name="GetSingleItem")
]