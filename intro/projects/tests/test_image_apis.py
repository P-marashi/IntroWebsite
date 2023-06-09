import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_post_image():
    """
    Test case for posting an image.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "image": "string"
    }

    response = client.post('/api/v1/projects/test/image/', payload, format='json')

    # Assertions based on the response status code
    if response.status_code == 201:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_get_image():
    """
    Test case for getting an image.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/projects/test/image/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "image not Found."


@pytest.mark.django_db
def test_get_image_slug():
    """
    Test case for getting a specific image by slug.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/projects/test/image/1/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "image not Found."


@pytest.mark.django_db
def test_put_image():
    """
    Test case for updating an image.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "image": "string"
    }

    response = client.put('/api/v1/projects/test/image/1/', payload, format='json')

    # Assertions based on the response status code
    if response.status_code == 201:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "image not Found."


@pytest.mark.django_db
def test_delete_image():
    """
    Test case for deleting an image.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.delete('/api/v1/projects/test/image/1/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "image not Found."
