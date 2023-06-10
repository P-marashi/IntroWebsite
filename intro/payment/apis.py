import requests

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from intro.core.serializers import VerifyURLSerializer, ErrorSerializer

from . import serializers
from . import models


ZARINPAL_REQUEST_URL = settings.ZARINPAL['default']['ZARINPAL_REQUEST_URL']
ZARINPAL_AUTHORITY_URL = settings.ZARINPAL['default']['ZARINPAL_AUTHORITY_URL']
MERCHANT_ID = settings.ZARINPAL['default']['MERCHANT_ID']
ZARINPAL_VERIFY_URL = settings.ZARINPAL['default']['ZARINPAL_VERIFY_URL']
CALLBACK_URL = settings.ZARINPAL['default']['CALLBACK_URL']


class SendPaymentRequestAPIView(APIView):
    """ An APIView for payment requests using zarinpal pg """

    serializer_class = {
        'request': serializers.TransactionRequestDataSerializer,
        'transaction': serializers.TransactionSerializer
    }
    model = models.Transaction
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=serializer_class['request'], responses={
        200: VerifyURLSerializer,
        400: ErrorSerializer
    })
    def post(self, request):
        """ Getting needed data using post request such as 'amount'
            and sending data to zarinpal payment gateway to recieve
            authority and pass it with zarinpal url to user for verification
        """
        # Getting needed data
        serializer = self.serializer_class['request'](data=request.data)
        # validating data
        serializer.is_valid(raise_exception=True)
        # getting needed data
        amount = serializer.validated_data.get('amount')
        phone = serializer.validated_data.get('phone')
        email = serializer.validated_data.get('email')
        description = serializer.validated_data.get('description')
        # generating data dictionary
        data = {
            'merchant_id': MERCHANT_ID,
            'callback_url': CALLBACK_URL,
            'amount': amount,
            'phone': phone,
            'email': email,
            'description': description
        }
        # sending data to zarinpal
        resp = requests.post(ZARINPAL_REQUEST_URL, data=data)
        # Storing object and returning url
        obj = self.model(
            amount=amount,
            phone=phone,
            email=email,
            description=description,
        )
        # Checking data results
        if resp.status_code == 200:
            authority = resp.json()['Authority']
            obj.authority = authority
            obj.save()
            return Response(VerifyURLSerializer({
                'url': ZARINPAL_AUTHORITY_URL.format(authority)
            }), status=status.HTTP_200_OK)
        # storing object as a failure payment and returning error
        obj.status = "F"
        obj.save()
        return Response(ErrorSerializer({
            "error": "Request to zarinpal Failed"
        }, status=status.HTTP_400_BAD_REQUEST))


class VerifyPaymentRequestAPIView(APIView):
    """ An [callback] APIView for verfication zarinpal payment request """

    serializer_class = {
        'request': serializers.TransationVerifyDataRequest,
        'transaction': serializers.TransactionSerializer
    }
    model = models.Transaction
    permission_classes = (IsAuthenticated,)

    def get(self, request, authority):
        """ Getting object by authority then sending needed data to zarinpal verify url
            then if the Status is 100, the object will store with success status and else
            the object will store with failure status
        """
        # Getting object by authority
        transaction = self.model.objects.get(authority=authority)
        # Declaring our neede data
        serializer = self.serializer_class['request'](data=request.data)
        # validating serializer
        serializer.is_valid(raise_exception=True)
        # getting needed data
        amount = serializer.validated_data.get('amount')
        authority = serializer.validated_data.get('authority')
        # set zarinpal verify data on dictionary
        data = {
            'merchant_id': MERCHANT_ID,
            'amount': amount,
            'authority': authority
        }
        # Sending request to zarinpal verify url
        resp = request.post(ZARINPAL_VERIFY_URL, data=data)
        # checking results
        if resp.status_code == 200:
            resp = resp.json()
            if resp.json()["Status"] == 100 or resp.json()["Status"] == 101:
                # storing object as a successfull payment
                transaction.status = "S"
                instance = transaction.save()
                # returning object in endpoint
                serializer = self.serializer_class['transaction'](instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            # storing object as a failure object
            transaction.status = "F"
            instance = transaction.save()
            # returning object
            return Response(self.serializer_class['transaction'](instance).data,
                            status=status.HTTP_400_BAD_REQUEST)
        # storing as failure and returning object
        transaction.status = "F"
        instance = transaction.save()
        return Response(self.serializer_class['transaction'](instance).data,
                        status=status.HTTP_400_BAD_REQUEST)
