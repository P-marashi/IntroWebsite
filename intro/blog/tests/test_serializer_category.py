import pytest
from myapp.serializers import BlogPostSerializer, CategorySerializer
from myapp.models import BlogPost, Category


@pytest.fixture
def sample_category_data():
    return {
        "name": "test Serializer"
    }


def test_category_serializer_valid_data(sample_category_data):
    # Create an instance of the CategorySerializer with sample data
    serializer = CategorySerializer(data=sample_category_data)

    # Assert that the serializer is valid and the validated data matches the sample data
    assert serializer.is_valid()
    assert serializer.validated_data == sample_category_data


def test_category_serializer_missing_required_field(sample_category_data):
    # Remove the 'name' field from the sample data
    del sample_category_data['name']

    # Create an instance of the CategorySerializer with modified sample data
    serializer = CategorySerializer(data=sample_category_data)

    # Assert that the serializer is not valid and 'name' field is present in the errors
    assert not serializer.is_valid()
    assert 'name' in serializer.errors
