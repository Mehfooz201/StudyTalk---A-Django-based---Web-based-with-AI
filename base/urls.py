from django.urls import path
from . import views

urlpatterns = [


    path('profile/<int:pk>/', views.userProfile, name='user-profile'),
    path('update-profile/', views.updateUser, name='update-profile'),


    path('login/', views.loginPage, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('rooms/<int:pk>/', views.rooms, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<int:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name='delete-room'),
    # path('search/', views.Search, name='search'),

    path('delete-message/<int:pk>/', views.deleteMessage, name='delete-message'),


    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
]
