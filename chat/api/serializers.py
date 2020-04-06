""" Module for manage serializers """

from rest_framework.serializers import ModelSerializer

from chat.models import Message, Thread


class MessageSerializer(ModelSerializer):
    """ Class to describe API Serializer """

    class Meta:
        model = Message
        fields = (
            'thread',
            'user',
            'creation_date',
            'body',
        )


class ThreadSerializer(ModelSerializer):
    """ Class to describe API Serializer """

    class Meta:
        model = Thread
        fields = (
            'patient',
            'doctor',
            'creation_date',
            'last_update',
            'status'
        )
