from django.urls import path
from .apis import (
    BlogPostCreateAPIView,
    BlogPostListAPIView,
    BlogPostRetrieveUpdateDestroyAPIView,
    CategoryAPIView,
    CategoryDetailAPI,
    CategoryListAPIView
)

urlpatterns = [
    # # Endpoint for creating a new  Category for blog post (admin only)
    path('category/', CategoryAPIView.as_view(), name='category'),
    path('category/list/', CategoryListAPIView.as_view(), name='category-list'),
    path('category/<slug:slug>/', CategoryDetailAPI.as_view(), name='category-retrieve-update-destroy'),
    # Endpoint for creating a new blog post (admin only)
    path('', BlogPostCreateAPIView.as_view(), name='blog-create'),

    # Endpoint for retrieving a list of all blog posts
    path('list/', BlogPostListAPIView.as_view(), name='blog-list'),

    # Endpoint for retrieving, updating, and deleting a specific blog post (admin only)
    path('<slug:slug>/', BlogPostRetrieveUpdateDestroyAPIView.as_view(),
         name='blog-retrieve-update-destroy'),
]
