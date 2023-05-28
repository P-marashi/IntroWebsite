from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.Serializer):
    """ Serializer for Chat model object """

    class Meta:
        model = Chat
        fields = [
            "sender",
            "anonymous_sender",
            "text",
        ]
