from django.http import Http404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema
from intro.core.serializers import EmptySerializer

from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostCreateAPIView(APIView):
    """
    API view for creating a new blog post.
    Only accessible by admin users.
    """

    permission_classes = [IsAdminUser]

    @extend_schema(request=EmptySerializer, responses={
        201: BlogPostSerializer})
    def post(self, request):
        """
        Create a new blog post.
        """

        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogPostListAPIView(APIView):
    """
    API view for retrieving a list of all blog posts.
    """

    @extend_schema(request=EmptySerializer, responses={
        200: BlogPostSerializer})
    def get(self, request):
        """
        Retrieve a list of all blog posts.
        """

        blog_posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data)


class BlogPostRetrieveUpdateDestroyAPIView(APIView):
    """
    API view for retrieving, updating, and deleting an individual blog post.
    Only accessible by admin users.
    """

    permission_classes = [IsAdminUser]

    def get_object(self, slug):
        """
        Get the blog post object based on the provided slug.
        """

        try:
            return BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            raise Http404

    @extend_schema(request=EmptySerializer, responses={
        200: BlogPostSerializer})
    def get(self, request, slug):
        """
        Retrieve the details of a blog post.
        """

        blog_post = self.get_object(slug)
        serializer = BlogPostSerializer(blog_post)
        return Response(serializer.data)

    @extend_schema(request=EmptySerializer, responses={
        200: BlogPostSerializer})
    def put(self, request, slug):
        """
        Update the details of a blog post.
        """

        blog_post = self.get_object(slug)
        serializer = BlogPostSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=EmptySerializer, responses={204: EmptySerializer})
    def delete(self, request, slug):
        """
        Delete a blog post.
        """

        blog_post = self.get_object(slug)
        blog_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
