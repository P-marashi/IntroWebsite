from rest_framework import serializers
from .models import Ticket, Answer


class TicketSerializer(serializers.ModelSerializer):
    # Set the user field as a hidden field and automatically populate it with the current user
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = '__all__'

    def get_user(self, obj):
        # Customize the serialized user information here
        user = obj.user
        return user

    def to_representation(self, instance):
        # Override the to_representation method to customize the serialized representation
        representation = super().to_representation(instance)
        representation['user'] = self.get_user(instance)
        return representation


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, validated_data):
        # Get the request object from the serializer context
        request = self.context.get('request')

        # Get the ticket instance from the validated data
        ticket = validated_data.get('ticket')

        # Check if the user making the request is an admin
        if request and request.user.is_superuser:
            # Set the ticket status to 'answered'
            ticket.status = 'answered'
            ticket.save()

            return super().create(validated_data)
        else:
            # Raise a validation error if a non-admin user tries to create an answer
            raise serializers.ValidationError("Only admin users can create answers.")
