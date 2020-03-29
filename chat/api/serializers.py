""" Module for manage serializers """

from rest_framework.serializers import ModelSerializer

from chat.models import Message


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
