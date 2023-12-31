import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_post_projects():
    """
    Test case for creating a project.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "title": "my Web",
        "slug": "test",
        "description": "this is for test",
        "url_example": "www.test.com",
    }

    response = client.post('/api/v1/projects/', payload, format='json')

    # Assertions based on the response status code
    if response.status_code == 201:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_get_projects():
    """
    Test case for retrieving projects.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/projects/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "projects not Found."


@pytest.mark.django_db
def test_get_projects_slug():
    """
    Test case for retrieving a project by slug.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/projects/1/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "projects not Found."


@pytest.mark.django_db
def test_put_projects():
    """
    Test case for updating a project.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "title": "my Web test put",
        "slug": "test",
        "description": "this is for test put",
        "url_example": "www.test-put.com",
    }

    response = client.put('/api/v1/projects/1/', payload, format='json')

    # Assertions based on the response status code
    if response.status_code == 201:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "projects not Found."


@pytest.mark.django_db
def test_delete_projects():
    """
    Test case for deleting a project.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.delete('/api/v1/projects/1/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "projects not Found."
