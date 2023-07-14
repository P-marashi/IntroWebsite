import pytest
from .serializers import ProjectSerializer, CommentSerializer, FeatureSerializer, ImageSerializer


@pytest.fixture
def sample_projects_post_data():
    return {
        'title': 'Test Projects Post',
        'slug': 'test',
        'features': 'Technology',
        'description': 'This is a test Projects post.',
        'url_example': 'www.test.com'
    }


def test_projects_post_serializer_valid_data(sample_projects_post_data):
    """
    Test case for validating the Projects serializer with valid data.
    """
    # Create an instance of the ProjectsPostSerializer with sample data
    serializer = ProjectSerializer(data=sample_projects_post_data)

    # Assert that the serializer is valid and the validated data matches the sample data
    assert serializer.is_valid()
    assert serializer.validated_data == sample_projects_post_data


def test_projects_post_serializer_missing_required_field(sample_projects_post_data):
    """
    Test case for validating the Projects serializer with missing required field.
    """
    # Remove the 'title' field from the sample data
    del sample_projects_post_data['title']

    # Create an instance of the ProjectsPostSerializer with modified sample data
    serializer = ProjectSerializer(data=sample_projects_post_data)

    # Assert that the serializer is not valid and 'title' field is present in the errors
    assert not serializer.is_valid()
    assert 'title' in serializer.errors


@pytest.fixture
def sample_comments_post_data():
    return {
        'title': 'Test Comments Post',
        'text': 'test-comments-post',
    }


def test_comments_post_serializer_valid_data(sample_comments_post_data):
    """
    Test case for validating the Comment serializer with valid data.
    """
    # Create an instance of the CommentSerializerPostSerializer with sample data
    serializer = CommentSerializer(data=sample_comments_post_data)

    # Assert that the serializer is valid and the validated data matches the sample data
    assert serializer.is_valid()
    assert serializer.validated_data == sample_comments_post_data


def test_comments_post_serializer_missing_required_field(sample_comments_post_data):
    """
    Test case for validating the Comment serializer with missing required field.
    """
    # Remove the 'title' field from the sample data
    del sample_comments_post_data['title']

    # Create an instance of the CommentSerializer with modified sample data
    serializer = CommentSerializer(data=sample_comments_post_data)

    # Assert that the serializer is not valid and 'title' field is present in the errors
    assert not serializer.is_valid()
    assert 'title' in serializer.errors


@pytest.fixture
def sample_features_post_data():
    return {
        'title': 'Test Features Post',
        'pk': 0,
    }


def test_features_post_serializer_valid_data(sample_features_post_data):
    """
    Test case for validating the Features serializer with valid data.
    """
    # Create an instance of the FeaturesPostSerializer with sample data
    serializer = FeatureSerializer(data=sample_features_post_data)

    # Assert that the serializer is valid and the validated data matches the sample data
    assert serializer.is_valid()
    assert serializer.validated_data == sample_features_post_data


def test_features_post_serializer_missing_required_field(sample_features_post_data):
    """
    Test case for validating the FeatureSerializer with missing required field.
    """
    # Remove the 'title' field from the sample data
    del sample_features_post_data['title']

    # Create an instance of the FeatureSerializer with modified sample data
    serializer = FeatureSerializer(data=sample_features_post_data)

    # Assert that the serializer is not valid and 'title' field is present in the errors
    assert not serializer.is_valid()
    assert 'title' in serializer.errors


@pytest.fixture
def sample_image_serializer_post_data():
    return {
        'image': 'path-image',
    }


def test_image_serializer_post_serializer_valid_data(sample_image_post_data):
    """
    Test case for validating the ImageSerializer with valid data.
    """
    # Create an instance of the ImageSerializer with sample data
    serializer = ImageSerializer(data=sample_image_post_data)

    # Assert that the serializer is valid and the validated data matches the sample data
    assert serializer.is_valid()
    assert serializer.validated_data == sample_image_post_data


def test_image_serializer_post_serializer_missing_required_field(sample_image_post_data):
    """
    Test case for validating the ImageSerializer with missing required field.
    """
    # Remove the 'image' field from the sample data
    del sample_image_post_data['image']

    # Create an instance of the ImageSerializer with modified sample data
    serializer = ImageSerializer(data=sample_image_post_data)

    # Assert that the serializer is not valid and 'image' field is present in the errors
    assert not serializer.is_valid()
    assert 'image' in serializer.errors
