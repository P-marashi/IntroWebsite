import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_category_post():
    client = APIClient()

    payload = {
        "name": "test"
    }

    response = client.get('/api/v1/blog/category/list', payload, format='json')

    assert response.status_code == 201

    assert response['name'] == payload['name']


@pytest.mark.django_db
def test_category_get():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    response = client.get('/api/v1/blog/category/list', format='json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_category_get_slug():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')
    response = client.get('/api/v1/blog/category/1/', format='json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_category_put():
    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')

    payload = {
        "name": "test_put"
    }

    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')
    response = client.put('/api/v1/blog/category/1/', format='json')

    assert response.status_code == 201

    assert response['name'] == payload['name']


@pytest.mark.django_db
def test_category_delete():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')
    response = client.delet('/api/v1/blog/category/1/', format='json')

    assert response.status_code == 200

