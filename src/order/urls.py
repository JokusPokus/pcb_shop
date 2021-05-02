from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('user/orders/', views.OrderList.as_view(), name='order_list'),
]
