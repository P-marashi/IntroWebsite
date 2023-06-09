import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from intro.core.models import BaseModel
from your_app.models import ImageExamples, Features, Projects, Comments


@pytest.mark.django_db
def test_image_examples_model():
    """
    Test case for the ImageExamples model.
    """
    # Create a temporary image file for testing
    image_path = 'path/to/your/image.jpg'
    image_file = SimpleUploadedFile(
        name='image.jpg',
        content=open(image_path, 'rb').read(),
        content_type='image/jpeg'
    )

    # Create an ImageExamples object with the temporary image file
    image = ImageExamples.objects.create(image=image_file)

    # Assertions
    assert isinstance(image, BaseModel)  # Check if the object is an instance of BaseModel
    assert str(image) == str(image.image)  # Check if the __str__ method returns the image path


@pytest.mark.django_db
def test_features_model():
    """
    Test case for the Features model.
    """
    # Create a Features object
    feature = Features.objects.create(title='Feature Title')

    # Assertions
    assert isinstance(feature, BaseModel)  # Check if the object is an instance of BaseModel
    assert str(feature) == feature.title  # Check if the __str__ method returns the feature title


@pytest.mark.django_db
def test_projects_model():
    """
    Test case for the Projects model.
    """
    # Create a user for testing
    user = settings.AUTH_USER_MODEL.objects.create(username='test_user')

    # Create a Projects object
    project = Projects.objects.create(
        title='Project Title',
        slug='project-slug',
        description='Project description',
        url_example='http://example.com',
        user=user
    )

    # Assertions
    assert isinstance(project, BaseModel)  # Check if the object is an instance of BaseModel
    assert str(project) == project.title  # Check if the __str__ method returns the project title


@pytest.mark.django_db
def test_comments_model():
    """
    Test case for the Comments model.
    """
    # Create a user for testing
    user = settings.AUTH_USER_MODEL.objects.create(username='test_user')

    # Create a Projects object for the comment to be associated with
    project = Projects.objects.create(
        title='Project Title',
        slug='project-slug',
        description='Project description',
        url_example='http://example.com',
        user=user
    )

    # Create a Comments object
    comment = Comments.objects.create(
        user=user,
        project=project,
        title='Comment Title',
        text='Comment text'
    )

    # Assertions
    assert isinstance(comment, BaseModel)  # Check if the object is an instance of BaseModel
    assert str(comment) == comment.title  # Check if the __str__ method returns the comment title
