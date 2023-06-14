from rest_framework import serializers
from . import models


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Ticket
        fields = ('id', 'parent',
                  'user', 'title',
                  'file', 'image',
                  'status', 'description',
                  )
