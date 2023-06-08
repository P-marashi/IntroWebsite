from django.http import Http404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from intro.core.serializers import EmptySerializer
from intro.utils.renderer import UserRenderer

from .models import BlogPost, Category
from .serializers import BlogPostSerializer, CategorySerializer


@extend_schema(request=EmptySerializer, responses={
    201: BlogPostSerializer}, tags=["Blog End-point"])
class CategoryAPIView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Blog End-point"])
class CategoryListAPIView(APIView):
    """
    API views for retrieving a list of all Category posts.
    """
    renderer_classes = [UserRenderer]

    @extend_schema(request=EmptySerializer, responses={
        200: CategorySerializer})
    def get(self, request):
        """
        Retrieve a list of all Category posts.
        """

        category_posts = Category.objects.all()
        serializer = CategorySerializer(Category, many=True)
        return Response(serializer.data)


@extend_schema(request=EmptySerializer, responses={
    201: BlogPostSerializer}, tags=["Blog End-point"])
class CategoryDetailAPI(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminUser]

    def get_object(self, slug):
        """
        Get the blog post object based on the provided slug.
        """

        try:
            return BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            raise NotFound

    @extend_schema(request=EmptySerializer, responses={
        200: BlogPostSerializer})
    def get(self, request, slug):
        """
        Retrieve the details of a blog post.
        """

        blog_post = self.get_object(slug)
        serializer = CategorySerializer(blog_post)
        return Response(serializer.data)

    @extend_schema(request=EmptySerializer, responses={
        200: BlogPostSerializer})
    def put(self, request, slug):
        """
        Update the details of a blog post.
        """

        blog_post = self.get_object(slug)
        serializer = CategorySerializer(blog_post, data=request.data)
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


@extend_schema(tags=["Blog End-point"])
class BlogPostCreateAPIView(APIView):
    """
    API views for creating a new blog post.
    Only accessible by admin users.
    """

    permission_classes = [IsAdminUser]
    renderer_classes = [UserRenderer]

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


@extend_schema(tags=["Blog End-point"])
class BlogPostListAPIView(APIView):
    """
    API views for retrieving a list of all blog posts.
    """
    renderer_classes = [UserRenderer]

    @extend_schema(request=EmptySerializer, responses={
        200: BlogPostSerializer})
    def get(self, request):
        """
        Retrieve a list of all blog posts.
        """

        blog_posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Blog End-point"])
class BlogPostRetrieveUpdateDestroyAPIView(APIView):
    """
    API views for retrieving, updating, and deleting an individual blog post.
    Only accessible by admin users.
    """

    renderer_classes = [UserRenderer]
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
