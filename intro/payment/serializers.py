from rest_framework import serializers

from .models import Transaction


class TransactionRequestDataSerializer(serializers.Serializer):
    """ A Serializer class for zarinpal request data """

    amount = serializers.IntegerField()
    phone = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    description = serializers.CharField(required=False)


class TransationVerifyDataRequest(serializers.Serializer):
    """ A Serializer class for zarinpal verify request data """

    amount = serializers.IntegerField()
    authority = serializers.CharField()


class TransactionSerializer(serializers.Serializer):
    """ A Serializer for Transaction model objects """

    class Meta:
        model = Transaction
        fields = [
            "title",
            "amount",
            "description",
            "user",
            "authority",
            "refID",
            "status",
        ]
