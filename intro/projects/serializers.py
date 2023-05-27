from rest_framework import serializers

from . import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageExamples
        fields = [
            "image",
            "updated_at",
            "created_at",
        ]


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Features
        fields = [
            "text",
            "updated_at",
            "created_at",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Projects
        fields = [
            "title",
            "slug",
            "description",
            "features",
            "images",
            "url_example",
            "updated_at",
            "created_at",
        ]
