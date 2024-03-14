from django.urls import path
from . import views

urlpatterns = [
    # GET 
    path("UserItems/all", views.GetAllUserItems, name="GetAllUserItems"),

    # GET
    # request.body parameter:
    #   int count: indicates numbers of each request should return
    path("Items/all", views.GetAllItems, name="GetAllItems"),

    path("Items/Collection/new", views.AddNewCollection, name="AddNewCollection"),

    path("Items/Collection", views.GetUserCollection, name="GetUserCollection"),

    # POST
    path("Item/new", views.CreateNewItem, name="CreateNewItem"),

    # GET PATCH DELETE
    path("Item/<uuid:item_id>", views.ProcessSingleItem, name="ProcessSingleItem"),

    path("Items/Search", views.SearchItems, name="SearchItems"),

    path("Items/Browse", views.BrowseOneKindItems, name="BrowseOneKindItems")

]