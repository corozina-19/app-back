""" Module to define API ViewSets """
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from rest_framework.parsers import JSONParser

from rest_framework.exceptions import ParseError

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from chat.api.serializers import MessageSerializer, ThreadSerializer
from chat.choices import open_, closed

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


class ThreadViewSet(ListModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]
    queryset = Thread.objects.all()
    parser_classes = [JSONParser]

    def get_permissions(self):
        """ Returns: list of permissions that vary depending on the user's role """
        permission_classes = [IsAuthenticated]
        if self.action in ['destroy']:
            permission_classes += [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """ A general filtering is done depending on the user, role and status of the thread """
        if not self.request.user.is_superuser:
            query = Thread.objects.filter(Q(doctor=self.request.user) | Q(patient=self.request.user))
        else:
            query = super().get_queryset()
        query = query.filter(status=open_)
        return query

    @action(methods=['GET'], detail=True, url_path='report-thread', url_name='report_thread')
    def report_thread(self, request, pk=None):
        """ This action is responsible for reporting a thread and placing it in a closed state. """
        instance = Thread.objects.get(id=pk)
        if instance.doctor == request.user:
            instance.status = closed
            instance.save()
            data = {'detail': "Closed thread", "status": HTTP_200_OK}
        else:
            data = {'detail': "403 Unauthorized", "status": HTTP_403_FORBIDDEN}
        return Response(data={"detail": data.get('detail')}, status=data.get('status'))

    @action(methods=['GET'], detail=True, url_path='close-thread', url_name='close_thread')
    def close_thread(self, request, pk=None):
        """ This action is responsible for closing a thread. """
        instance = Thread.objects.get(id=pk)
        if request.user in (instance.doctor, instance.patient):
            instance.status = closed
            instance.save()
            data = {'detail': "Closed thread", "status": HTTP_200_OK}
        else:
            data = {'detail': "403 Unauthorized", "status": HTTP_403_FORBIDDEN}
        return Response(data={"detail": data.get('detail')}, status=data.get('status'))

    @action(methods=['GET'], detail=True, url_path='take-thread', url_name='take_thread')
    def take_thread(self, request, pk=None):
        """ This action is responsible for assigning a thread without a doctor to the authenticated user. """
        instance = Thread.objects.get(id=pk)
        if not instance.doctor:
            instance.doctor = request.user
            instance.save()
            data = {'detail': "Take thread", "status": HTTP_200_OK}
        else:
            data = {'detail': "404 Not found", "status": HTTP_404_NOT_FOUND}
        return Response(data={"detail": data.get('detail')}, status=data.get('status'))
