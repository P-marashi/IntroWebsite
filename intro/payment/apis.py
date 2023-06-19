from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from intro.core.serializers import VerifyURLSerializer, ErrorSerializer

from . import serializers
from . import models
from .zarinpal import zarinpal


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
        # Storing object
        obj = self.model(
            amount=amount,
            user=request.user,
            description=description,
        )
        # Sending request to payment gateway
        response = zarinpal.send_request(amount=amount,
                                         description="Transaction Description",
                                         email=email, phone=phone)
        if response:
            # Storing object
            obj.authority = response
            obj.save()
            return Response(VerifyURLSerializer({
                'url': zarinpal.authority_url + response
            }).data)
        # storing object as a failure payment and returning error
        obj.status = "F"
        obj.save()
        return Response(ErrorSerializer({
            "error": "Request to zarinpal Failed"
        }).data, status=status.HTTP_400_BAD_REQUEST)


class VerifyPaymentRequestAPIView(APIView):
    """ An [callback] APIView for verfication zarinpal payment request """

    serializer_class = serializers.TransactionSerializer
    model = models.Transaction
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ Getting object by authority then sending needed data to zarinpal verify url
            then if the Status is 100, the object will store with success status and else
            the object will store with failure status
        """
        # Getting object by authority
        authority = request.query_params.get('Authority')
        transaction = self.model.objects.get(authority=authority)
        # Send request to payment gateway
        resp = zarinpal.send_verify(transaction.amount, authority)
        # checking results
        if resp:
            # storing object as a successfull payment
            transaction.refID = resp
            transaction.status = "S"
            transaction.save()
            # returning object in endpoint
            serializer = self.serializer_class(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # storing as failure and returning object
        transaction.status = "F"
        transaction.save()
        return Response(self.serializer_class(transaction).data,
                        status=status.HTTP_400_BAD_REQUEST)
