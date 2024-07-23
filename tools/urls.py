from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', include('app.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    
]
