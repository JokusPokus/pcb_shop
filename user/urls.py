from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('info/', views.UserDetails.as_view(), name='user_details'),
    path('attributes/addresses/', views.AddressList.as_view(), name='address_list'),
    path('attributes/addresses/<int:pk>/', views.AddressDetails.as_view(), name='address_details'),
    path('attributes/addresses/change-default/', views.change_address_default, name='change_address_default'),
    path('basket/', views.BasketItemList.as_view(), name='basket_items'),
    path('basket/<int:pk>/', views.BasketItemDetails.as_view(), name='basket_item_details'),
]
