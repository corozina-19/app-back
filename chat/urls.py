""" Module to define url for chat """
from django.urls import path
from django.urls import include

app_name = 'chat'
urlpatterns = [
    path('', include('chat.api.urls')),
]
