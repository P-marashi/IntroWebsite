import pytest
from myapp.serializers import BlogPostSerializer, CategorySerializer
from myapp.models import BlogPost, Category


@pytest.fixture
def sample_blog_post_data():
    return {
        'title': 'Test Blog Post',
        'slug': 'test-blog-post',
        'category': 'Technology',
        'text': 'This is a test blog post.',
    }


def test_blog_post_serializer_valid_data(sample_blog_post_data):
    serializer = BlogPostSerializer(data=sample_blog_post_data)
    assert serializer.is_valid()
    assert serializer.validated_data == sample_blog_post_data


def test_blog_post_serializer_missing_required_field(sample_blog_post_data):
    del sample_blog_post_data['title']
    serializer = BlogPostSerializer(data=sample_blog_post_data)
    assert not serializer.is_valid()
    assert 'title' in serializer.errors

# Add more test functions as needed for other serializer methods or scenarios
