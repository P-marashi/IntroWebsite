import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_post_tickets():
    client = APIClient()

    # Set authentication credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "title": "test",
        "description": "this is for test"
    }

    response = client.post('/api/v1/support/tickets/', payload, format='json')

    if response.status_code == 201:
        assert response.data['title'] == payload['title']
        assert response.data['description'] == payload['description']
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_get_all_tickets():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/support/tickets/', format='json')

    if response.status_code == 200:
        assert response.data['status'] == "success"
    elif response.status_code == 404:
        assert response.data['status'] == "error"
        assert response.data["message"] == "No Tickets found"
    elif response.status_code == 401:
        assert response.data['status'] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_get_tickets():
    client = APIClient()

    # Set authentication credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/support/tickets/1/', format='json')

    if response.status_code == 200:
        assert response.data['success'] == "success"
    elif response.status_code == 401:
        assert response.data['status'] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["message"] == "No tickets found"


@pytest.mark.django_db
def test_put_blog():
    client = APIClient()

    # Set authentication credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "title": "testing the put request",
        "description": "this is for test"
    }

    response = client.patch('/api/v1/support/tickets/2/', payload, format='json')

    if response.status_code == 201:
        assert response.data['title'] == payload['title']
        assert response.data['description'] == payload['description']
    elif response.status_code == 401:
        assert response.data['status'] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_delete_blog():
    client = APIClient()

    # Set authentication credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.delete('/api/v1/support/tickets/2/', format='json')

    if response.status_code == 200:
        assert response.data['success'] == "success"
    elif response.status_code == 401:
        assert response.data['status'] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["message"] == "No tickets found"
