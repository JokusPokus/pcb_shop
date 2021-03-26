from django.urls import path

from . import views

app_name = 'article'

urlpatterns = [
    path('', views.BoardList.as_view(), name='board_list'),
]
