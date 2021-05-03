from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('user/info/', views.UserDetails.as_view(), name='user_details'),
    path('user/addresses/', views.AddressList.as_view(), name='address_list'),
    path('user/addresses/<int:pk>/', views.AddressDetails.as_view(), name='address_details'),
    path('user/addresses/change-default/', views.change_address_default, name='change_address_default'),
    path('shop/user/basket/', views.BasketItemList.as_view(), name='basket_items'),
    path('shop/user/basket/<int:article_pk>/', views.BasketItemDetails.as_view(), name='basket_item_details'),
]
