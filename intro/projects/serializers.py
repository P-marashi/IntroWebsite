from rest_framework import serializers

from . import models


class ImageSerializer(serializers.ModelSerializer):
    """ Serializing the images of projects """

    class Meta:
        model = models.ImageExamples
        fields = [
            "pk",
            "image",
        ]


class FeatureSerializer(serializers.ModelSerializer):
    """ Serializing the feature of projects """
    class Meta:
        model = models.Features
        fields = [
            "pk",
            "title"
        ]


class ProjectSerializer(serializers.ModelSerializer):
    """ Serializing the projects """
    class Meta:
        model = models.Projects
        fields = [
            "pk",
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


class CommentSerializer(serializers.ModelSerializer):
    """ Comment serializer for each project """
    class Meta:
        model = models.Comments
        fields = [
            "pk",
            "title",
            "text",
        ]
