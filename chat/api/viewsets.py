""" Module to define API ViewSets """
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework.parsers import JSONParser

from rest_framework.exceptions import ParseError

from rest_framework.permissions import IsAuthenticated

from chat.api.serializers import MessageSerializer

from chat.models import Thread
from chat.models import Message


class MessageViewSet(CreateModelMixin, GenericViewSet):
    """ Message ViewSet only manage message creation is not allowed to do more """
    model = Message
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
        """ Override standard method to insert thread creation logic """
        values = list(request.data.values())
        if not any(values) or 'thread' not in request.data:
            raise ParseError(detail='Bad formed message information.')

        if not request.data['thread']:
            thread = Thread.objects.create(
                patient=request.user,
            )
            request.data['thread'] = thread.id
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

