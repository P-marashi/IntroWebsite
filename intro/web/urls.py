from django.urls import path

from . import apis


urlpatterns = [
    path('', apis.IndexAPIView.as_view(), name="index"),
    path('dashboard/', apis.DashboardAPIView.as_view(), name="dashboard")
]
