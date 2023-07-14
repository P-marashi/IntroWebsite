import pytest
from rest_framework.test import APIClient
from intro.support.serializers import TicketSerializer


@pytest.fixture
def sample_support_post_data():
    return {
        'title': 'Test support Post',
        'description': 'test support  post',
        'category': 'Technology',
        'text': 'This is a test support post.',
    }


def test_support_post_serializer_valid_data(sample_support_post_data):
    # Create an instance of the TicketSerializer with sample data
    serializer = TicketSerializer(data=sample_support_post_data)

    # Assert that the serializer is valid and the validated data matches the sample data
    assert serializer.is_valid()
    assert serializer.validated_data == sample_support_post_data


def test_support_post_serializer_missing_required_field(sample_support_post_data):
    # Remove the 'title' field from the sample data
    del sample_support_post_data['title']

    # Create an instance of the TicketSerializer with modified sample data
    serializer = TicketSerializer(data=sample_support_post_data)

    # Assert that the serializer is not valid and 'title' field is present in the errors
    assert not serializer.is_valid()
    assert 'title' in serializer.errors
