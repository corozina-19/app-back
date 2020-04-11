""" Module for define urls """
from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

from chat.api import viewsets as api_views

router = DefaultRouter()
router.register('message', api_views.MessageViewSet, basename='message')
router.register('thread', api_views.ThreadViewSet, basename='thread')

urlpatterns = [
    path('', include(router.urls)),
]
