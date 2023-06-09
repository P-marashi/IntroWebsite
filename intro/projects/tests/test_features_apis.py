import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_post_features():
    """
    Test case for creating a new feature.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "title": "my Web",
        "pk": 0,
    }

    response = client.post('/api/v1/projects/test/features/', payload, format='json')

    # Assertions based on the response status code
    if response.status_code == 201:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_get_features():
    """
    Test case for retrieving all features.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/projects/test/features/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "features not Found."


@pytest.mark.django_db
def test_get_features_slug():
    """
    Test case for retrieving a specific feature.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/projects/test/features/1/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "features not Found."


@pytest.mark.django_db
def test_put_features():
    """
    Test case for updating a feature.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "title": "my Web test put",
        "pk": 0,
    }
    response = client.put('/api/v1/projects/test/features/1/', payload, format='json')

    # Assertions based on the response status code
    if response.status_code == 201:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "features not Found."


@pytest.mark.django_db
def test_delete_features():
    """
    Test case for deleting a feature.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.delete('/api/v1/projects/test/features/1/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "features not Found."
