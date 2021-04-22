from django.urls import path

from . import views

app_name = 'price'

urlpatterns = [
    path('', views.calculate_board_price, name='board_price'),
]
