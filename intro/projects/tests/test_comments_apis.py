import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_post_comments():
    """
    Test case for creating a new comment.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "pk": 0,
        "title": "test comments",
        "text": "test"
    }

    response = client.post('/api/v1/projects/test/comments/', payload, format='json')

    # Assertions based on the response status code
    if response.status_code == 201:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_get_comments():
    """
    Test case for retrieving all comments.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/projects/test/comments/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "comments not Found."


@pytest.mark.django_db
def test_get_comments_slug():
    """
    Test case for retrieving a specific comment.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/projects/test/comments/1/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "comments not Found."


@pytest.mark.django_db
def test_put_comments():
    """
    Test case for updating a comment.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "pk": 0,
        "title": "test comments",
        "text": "test"
    }

    response = client.put('/api/v1/projects/test/comments/1/', payload, format='json')

    # Assertions based on the response status code
    if response.status_code == 201:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "comments not Found."


@pytest.mark.django_db
def test_delete_comments():
    """
    Test case for deleting a comment.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.delete('/api/v1/projects/test/comments/1/', format='json')

    # Assertions based on the response status code
    if response.status_code == 200:
        assert response.data["status"]
