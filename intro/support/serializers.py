from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models
from intro.users.serializers import UserSerializer


class UserInfoSerailzer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "phone_number",
            "email",
        ]


class TicketSerializer(serializers.ModelSerializer):
    user = UserInfoSerailzer()

    class Meta:
        model = models.Ticket
        fields = ('id', 'parent',
                  'user', 'title',
                  'file', 'image',
                  'status', 'description',
                  )
