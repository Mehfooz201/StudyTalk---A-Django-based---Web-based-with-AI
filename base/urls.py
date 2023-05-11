from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/<int:pk>/', views.rooms, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<int:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name='delete-room'),
]
