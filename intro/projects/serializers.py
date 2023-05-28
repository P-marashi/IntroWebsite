from rest_framework import serializers

from . import models


class ImageSerializer(serializers.ModelSerializer):
    """ Serializing the images of projects """

    class Meta:
        model = models.ImageExamples
        fields = [
            "image",
            "updated_at",
            "created_at",
        ]


class FeatureSerializer(serializers.ModelSerializer):
    """ Serializing the feature of projects """
    class Meta:
        model = models.Features
        fields = [
            "text",
            "updated_at",
            "created_at",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    """ Serializing the projects """
    class Meta:
        model = models.Projects
        fields = [
            "title",
            "slug",
            "description",
            "features",
            "images",
            "url_example",
            "user",
            "updated_at",
            "created_at",
        ]
