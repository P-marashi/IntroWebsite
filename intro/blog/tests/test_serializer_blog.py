import pytest
from .serializers import BlogPostSerializer, CategorySerializer



@pytest.fixture
def sample_blog_post_data():
    return {
        'title': 'Test Blog Post',
        'slug': 'test-blog-post',
        'category': 'Technology',
        'text': 'This is a test blog post.',
    }


def test_blog_post_serializer_valid_data(sample_blog_post_data):
    # Create an instance of the BlogPostSerializer with sample data
    serializer = BlogPostSerializer(data=sample_blog_post_data)

    # Assert that the serializer is valid and the validated data matches the sample data
    assert serializer.is_valid()
    assert serializer.validated_data == sample_blog_post_data


def test_blog_post_serializer_missing_required_field(sample_blog_post_data):
    # Remove the 'title' field from the sample data
    del sample_blog_post_data['title']

    # Create an instance of the BlogPostSerializer with modified sample data
    serializer = BlogPostSerializer(data=sample_blog_post_data)

    # Assert that the serializer is not valid and 'title' field is present in the errors
    assert not serializer.is_valid()
    assert 'title' in serializer.errors
