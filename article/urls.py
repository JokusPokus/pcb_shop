from django.urls import path

from . import views

app_name = 'article'

urlpatterns = [
    path('users/<int:user_pk>/boards/', views.BoardList.as_view(), name='board_list'),
    # path('users/<int:user_pk>/boards/', views.UserDetails.as_view(), name='user_details')
]
