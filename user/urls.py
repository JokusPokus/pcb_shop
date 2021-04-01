from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('info/', views.UserDetails.as_view(), name='user_details'),
    path('attributes/addresses/', views.AddressList.as_view(), name='address_list'),
    path('attributes/default-shipping-address/', views.DefaultShippingAddressDetails.as_view(), name='shipping_address'),
    path('attributes/default-billing-address/', views.DefaultBillingAddressDetails.as_view(), name='shipping_address'),
]
