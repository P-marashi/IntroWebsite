from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    """ An Empty serializer for non-required
        data to recieve or response apis
    """

    ...


class VerifyURLSerializer(serializers.Serializer):
    """ Serializer for response Url to user """

    url = serializers.URLField()


class ErrorSerializer(serializers.Serializer):
    """ Serializer for response error to user """

    error = serializers.CharField()