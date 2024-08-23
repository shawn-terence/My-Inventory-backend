
from django.contrib import admin
from django.urls import path
from api.views import *
urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/",UserRegistrationView.as_view(),name="register"),
    path("login/",UserLoginView.as_view(),name="login"),
    path("inventory/add/",AddInventoryView.as_view(),name="add_asset"),
    path("inventory/",InventoryListView.as_view(),name="list_asset"),
    path("buy/",PurchaseView.as_view(),name="buy"),
    path("update/<int:pk>/add/",UpdateInventoryView.as_view(),name="add_stock"),
    path('upload/', upload_file_view, name='upload_file'),
    path("inventory/<int:pk>/delete",DeleteInventoryView.as_view(),name="delete_item"),
    path("purchase/",PurchaseView.as_view(),name="purchase"),
    path("transactions/",TransactionsView.as_view(),name="transactions")
]
