import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_post_category():
    # Create an instance of the APIClient
    client = APIClient()

    # Set the authorization credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    # Define the payload for the POST request
    payload = {
        "name": "test"
    }

    # Send a POST request to create a new category
    response = client.post('/api/v1/blog/category/', payload, format='json')

    # Check the response status code and validate the data accordingly
    if response.status_code == 201:
        assert response.data['name'] == payload['name']
    elif response.status_code == 401:
        assert response.data['status'] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_get_category():
    # Create an instance of the APIClient
    client = APIClient()

    # Send a GET request to retrieve all categories
    response = client.get('/api/v1/blog/category/list', format='json')

    # Check the response status code and validate the data accordingly
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "category not Found."


@pytest.mark.django_db
def test_category_get_slug():
    # Create an instance of the APIClient
    client = APIClient()

    # Set the authorization credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    # Send a GET request to retrieve a category by slug
    response = client.get('/api/v1/blog/category/1/', format='json')

    # Check the response status code and validate the data accordingly
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "category not Found."


@pytest.mark.django_db
def test_category_put():
    # Create an instance of the APIClient
    client = APIClient()

    # Set the authorization credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    # Define the payload for the PUT request
    payload = {
        "name": "test_put"
    }

    # Send a PUT request to update a category
    response = client.put('/api/v1/blog/category/1/', payload, format='json')

    # Check the response status code and validate the data accordingly
    if response.status_code == 201:
        assert response.data['name'] == payload['name']
    elif response.status_code == 401:
        assert response.data['status'] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "category not Found."


@pytest.mark.django_db
def test_category_delete():
    # Create an instance of the APIClient
    client = APIClient()

    # Set the authorization credentials
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    # Send a DELETE request to delete a category
    response = client.delete('/api/v1/blog/category/1/', format='json')

    # Check the response status code and validate the data accordingly
    if response.status_code == 200:
        assert response.data["status"] == "success"
    elif response.status_code == 401:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Authentication credentials were not provided."
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "category not Found."
