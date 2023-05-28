from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """
    Serializer for the BlogPost model.
    """

    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'category', 'image', 'text']
