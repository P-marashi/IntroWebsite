from django.urls import path
from .apis import (
    BlogPostCreateAPIView,
    BlogPostListAPIView,
    BlogPostDetailAPIView
)

urlpatterns = [
    # Endpoint for creating a new blog post (admin only)
    path('blog/', BlogPostCreateAPIView.as_view(), name='blog-create'),

    # Endpoint for retrieving a list of all blog posts
    path('blog/list/', BlogPostListAPIView.as_view(), name='blog-list'),

    # Endpoint for retrieving, updating, and deleting a specific blog post (admin only)
    path('blog/<slug:slug>/', BlogPostDetailAPIView.as_view(), name='blog-detail'),
]
