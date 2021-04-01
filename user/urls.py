from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('info/', views.UserDetails.as_view(), name='user_details'),
    path('attributes/billing-addresses/', views.BillingAddressList.as_view(), name='billing_address_list'),
    path('attributes/shipping-addresses/', views.ShippingAddressList.as_view(), name='shipping_address_list'),
]
