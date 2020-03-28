""" Module to define API ViewSets """
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework.permissions import IsAuthenticated

from chat.models import Message


class MessageViewSet(CreateModelMixin, GenericViewSet):
    """ Message ViewSet only manage message creation is not allowed to do more """
    model = Message
    permission_classes = [IsAuthenticated]

    class Meta:
        model = Message
