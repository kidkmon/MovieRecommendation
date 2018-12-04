from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('movie/<int:pk>/', views.post_detail, name='post_detail'),
    path('movie/genre', views.genre, name='post_edit'),
]