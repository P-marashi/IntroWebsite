from django.urls import path
from .apis import (
    BlogPostCreateAPIView,
    BlogPostListAPIView,
    BlogPostDetailAPIView
)

urlpatterns = [
    # Endpoint for creating a new blog post (admin only)
    path('', BlogPostCreateAPIView.as_view(), name='blog-create'),

    # Endpoint for retrieving a list of all blog posts
    path('list/', BlogPostListAPIView.as_view(), name='blog-list'),

    # Endpoint for retrieving, updating, and deleting a specific blog post (admin only)
    path('<slug:slug>/', BlogPostDetailAPIView.as_view(), name='blog-detail'),
]
