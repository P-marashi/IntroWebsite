from rest_framework import serializers
from .models import BlogPost, Category


class BlogPostSerializer(serializers.ModelSerializer):
    """
    Serializer for the BlogPost model.
    """

    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'category', 'image', 'text']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:

        model = Category
        fields = ('name',)
