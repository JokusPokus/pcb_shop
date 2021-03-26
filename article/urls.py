from django.urls import path

from . import views

app_name = 'article'

urlpatterns = [
    path('user/boards/', views.BoardList.as_view(), name='board_list'),
    path('user/boards/<int:pk>/', views.BoardDetails.as_view(), name='user_details')
]
