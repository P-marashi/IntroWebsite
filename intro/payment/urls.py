from django.urls import path
from . import apis


urlpatterns = [
    path('request/', apis.SendPaymentRequestAPIView.as_view(), name="request"),
    path('verify/<str:authority>/', apis.VerifyPaymentRequestAPIView.as_view(),
         name="verify")
]
