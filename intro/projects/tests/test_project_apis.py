# import pytest
# from rest_framework.test import APIClient
#
#
# @pytest.mark.django_db
# def test_post_projects():
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')
#
#     payload = {
#         "title": "my Web",
#         "slug": "my Web",
#         "description": "this is for test",
#         "features": "im want test",
#         "images": "",
#         "url_example": "www.damailn.com",
#     }
#
#     response = client.post('/api/v1/projects/', payload, format='json')
#
#     if response.status_code == 201:
#         assert response.data["status"] == "success"
#     elif response.status_code == 401:
#         assert response.data["status"] == "error"
#         assert response.data["message"] == "Authentication credentials were not provided."
#
#
# @pytest.mark.django_db
# def test_post_projects():
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION='Bearer your_access_token')
#
#     response = client.get('/api/v1/projects/', format='json')
#
#     if response.status_code == 200:
#         assert response.data["status"] == "success"
#
#     elif response.status_code == 401:
#         assert response.data["status"] == "error"
#         assert response.data["message"] == "Authentication credentials were not provided."
#
#     elif response.status_code == 404:
#         assert response.data["status"] == "error"
#         assert response.data["message"] == "projects not Found."
