import pytest
from myapp.serializers import BlogPostSerializer, CategorySerializer
from myapp.models import BlogPost, Category


@pytest.fixture
def sample_category_data():
    return {
        "name": "test Serialzer"
    }


def test_category_serialzer(sample_category_data):
    serializer = CategorySerializer(data=sample_category_data)
    assert serializer.is_valid()
    assert serializer.validated_data == sample_category_data


def test_category_serializer_misssing_required_field(sample_category_data):
    del sample_category_data['name']
    serializer = CategorySerializer(data=sample_category_data)
    assert not serializer.is_valid()
    assert "title" in serializer.errors
