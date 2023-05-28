from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    """ An Empty serializer for non-required
        data to recieve or response apis
    """

    ...
