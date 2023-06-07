import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_post_blog():
    client = APIClient()

    # Set authentication credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "title": "this is test",
        "slug": "this is test",
        "category": "1",
        "text": "fk this lig"
    }

    response = client.post('/api/v1/blog/', payload, format='json')

    if response.status_code == 201:
        assert response.data['title'] == payload['title']
        assert response.data['slug'] == payload['slug']
        assert response.data['category'] == payload['category']
        assert response.data['text'] == payload['text']
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_get_all_blog():
    client = APIClient()

    response = client.get('/api/v1/blog/', format='json')

    if response.status_code == 200:
        assert response.data['status'] == "success"
    elif response.status_code == 404:
        assert response.data['status'] == "error"
        assert response.data["message"] == "No blog found"


@pytest.mark.django_db
def test_get_blog():
    client = APIClient()

    # Set authentication credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/blog/1/', format='json')

    if response.status_code == 200:
        assert response.data['success'] == "success"
    elif response.status_code == 401:
        assert response.data['status'] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["message"] == "No blog found"


@pytest.mark.django_db
def test_put_blog():
    client = APIClient()

    # Set authentication credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "title": "this is test",
        "slug": "this is test",
        "category": "1",
        "text": "fk this lig"
    }

    response = client.put('/api/v1/blog/1/', payload, format='json')

    if response.status_code == 201:
        assert response.data['title'] == payload['title']
        assert response.data['slug'] == payload['slug']
        assert response.data['category'] == payload['category']
        assert response.data['text'] == payload['text']
    elif response.status_code == 401:
        assert response.data['status'] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_delete_blog():
    client = APIClient()

    # Set authentication credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.delete('/api/v1/blog/1/', format='json')

    if response.status_code == 200:
        assert response.data['success'] == "success"
    elif response.status_code == 401:
        assert response.data['status'] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["message"] == "No blog found"
