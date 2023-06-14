import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_user():
    client = APIClient()

    # Set authentication credentials

    payload = {
        "login_method": "puyamarashii@gmail.com",
        "password": "p12345678p",
        "password_confirm": "p12345678p"
    }

    response = client.post('/api/v1/auth/register/', payload, format='json')

    if response.status_code == 201:
        assert response.data['login_method'] == payload['login_method']
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "Page NOT Found"


@pytest.mark.django_db
def test_login_user():
    client = APIClient()

    # Set authentication credentials

    payload = {
        "login_method": "puyamarashii@gmail.com",
        "password": "p12345678p"
    }

    response = client.post('/api/v1/auth/login/', payload, format='json')

    if response.status_code == 200:
        assert response.data['login_method'] == payload['login_method']
    elif response.status_code == 404:
        assert response.data["status"] == "error"
        assert response.data["message"] == "User NOT Found"
