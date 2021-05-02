from django.urls import path

from . import views

app_name = 'article'

urlpatterns = [
    path('user/boards/', views.BoardList.as_view(), name='board_list'),
    path('user/boards/<int:pk>/', views.BoardDetails.as_view(), name='board_details'),
    path('board-configurator/available-options/', views.BoardOptions.as_view(), name='board_options'),
]
