from django.urls import path
from . import views

urlpatterns = [
    # GET 
    path("UserItems/all", views.GetAllUserItems, name="GetAllUserItems"),

    # GET
    # request.body parameter:
    #   int count: indicates numbers of each request should return
    path("Items/all", views.GetAllItems, name="GetAllItems"),

    path("Items/user/all", views.GetAllItemsByDistance, name="GetAllItemsByDistance"),

    path("Items/Collection/new/<uuid:item_id>", views.AddNewCollection, name="AddNewCollection"),

    path("Items/Collection", views.GetUserCollection, name="GetUserCollection"),

    path("Items/Collection/delete/<uuid:item_id>", views.DeleteUserCollection, name="DeleteUserCollection"),

    path("Items/Collection/item/<uuid:item_id>", views.IsUserCollected, name="IsUserCollected"),

    # POST
    path("Item/new", views.CreateNewItem, name="CreateNewItem"),


    # GET PATCH DELETE
    path("Item/<uuid:item_id>", views.ProcessSingleItem, name="ProcessSingleItem"),

    path("Items/Search", views.SearchItems, name="SearchItems"),

    path("Items/Browse", views.BrowseOneKindItems, name="BrowseOneKindItems"),

    path("Order/Transactions/all", views.GetAllTransactions, name="GetAllTransactions"),

    path("Order/Transaction/new", views.SaveTransaction, name="SaveTransaction"),

    path("Order/Transaction/Review/<int:user_id>", views.GetUserReviews, name="GetUserReviews"),

    path("Order/Transaction/Review/add/<uuid:order_id>", views.WriteReview, name="WriteReview"),

    path("Order/Transaction/Review/UnReviewedOrder", views.GetUnReviewedOrder, name="GetUnReviewedOrder"),

]