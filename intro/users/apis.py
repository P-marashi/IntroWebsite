from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_spectacular.utils import extend_schema, OpenApiParameter

from intro.utils.regexes import is_phone_or_email
from intro.utils.otp import otp_generator

from intro.core.serializers import EmptySerializer
from intro.core.tokens import one_time_token_generator
from intro.core.cache import cache_otp
from intro.core.tasks import send_otp_email, send_otp_mobile

from . import serializers

from .backends import AUTH


# declared needed api paramteres on @extend_schema
ONE_TIME_LINK_API_PARAMETERS = [
    OpenApiParameter(
        'uidb64',
        type=str,
        location=OpenApiParameter.PATH,
        description="user primary key that encoded to base64",
    ),
    OpenApiParameter(
        'token',
        type=str,
        location=OpenApiParameter.PATH,
        description="one time generated token"
    )
]


class Login(APIView):
    """ an APIView for users logging in
        check user login_method and password
        then Generate jwt token
    """

    permission_classes = (AllowAny, )

    @extend_schema(request=serializers.LoginSerializer, responses={
        200: serializers.TokenSerializer,
        404: serializers.ErrorSerializer})
    def post(self, request):
        """ Accept post request for logging in """
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_method = serializer.validated_data.get('login_method')
        password = serializer.validated_data.get('password')
        user = AUTH.authenticate(request, is_phone_or_email(login_method),
                                 password=password)
        if user.is_active:
            tokens = AUTH.generate_token(user)
            return Response(data=serializers.TokenSerializer(tokens),
                            status=status.HTTP_200_OK)
        return Response(data=serializers.ErrorSerializer({
            'error': 'User not found'
        }), status=status.HTTP_404_NOT_FOUND)


class Register(APIView):
    """ An APIView for users registration
        send otp code to email/phone
        generate activation url and return it
    """

    permission_classes = (AllowAny, )

    @extend_schema(request=serializers.RegisterSerializer, responses={
        201: serializers.VerifyURLSerializer})
    def post(self, request):
        """ Accept post request for registering users """
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_method = serializer.validated_data.get('login_method')
        password = serializer.validated_data.get('password')
        phone_or_email = is_phone_or_email(login_method)
        otp = otp_generator
        cache_otp(login_method, otp)
        if phone_or_email == "email":
            user = get_user_model().objects.create_user(email=login_method,
                                                        password=password)
            send_otp_email.delay(login_method, otp)
        elif phone_or_email == "phone":
            user = get_user_model().objects.create_user(
                phone_number=login_method, password=password)
            send_otp_mobile.delay(login_method, otp)
        url = one_time_token_generator.make_token(user)
        return Response(data=serializers.VerifyURLSerializer(
            {'url': url}
        ), status=status.HTTP_201_CREATED)


class VerifyRegsiter(APIView):
    """ An APIView for verify users registration
        gives user otp code and validate it
        set user is active eq to True
        return User object
    """

    permission_classes = (AllowAny, )

    @extend_schema(request=serializers.RegisterVerifySerializer, responses={
        200: serializers.UserSerializer,
        403: serializers.ErrorSerializer
    }, parameters=ONE_TIME_LINK_API_PARAMETERS)
    def post(self, request, uidb64, token):
        """ Accept post request for verifying users registration """
        user = one_time_token_generator.decode_token(uidb64)
        if user and one_time_token_generator.check_token(token):
            serializer = serializers.RegisterVerifySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            login_method = serializer.validated_data.get('login_method')
            user = get_user_model().objects.get(
                Q(email=login_method) | Q(phone_number=login_method)
            )
            user.is_active = True
            user.save()
            return Response(data=serializers.UserSerializer(user),
                            status=status.HTTP_200_OK)
        return Response(data=serializers.ErrorSerializer({
            'error': 'Url activation token is expired.'
        }), status=status.HTTP_403_FORBIDDEN)


class ChangePassword(APIView):
    """ An APIView for changing users passwords
        check users old password
        matching users new password and password confirm
        set users new password
    """
    permission_classes = (IsAuthenticated, )

    @extend_schema(request=serializers.ChangePasswordSerializer, responses={
        200: serializers.UserSerializer})
    def put(self, request):
        """ Accept put request for changing users password """
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password_confirm')
        request.user.set_password(password)
        request.user.save()
        return Response(data=serializers.UserSerializer(request.user),
                        status=status.HTTP_200_OK)


class ResetPassword(APIView):
    """ An APIView for reset users passwords
        gives email/phone number from user
        then send a code to that email/phone
        for verification
    """

    permission_classes = (AllowAny, )

    @extend_schema(request=serializers.ResetPasswordSerializer, responses={
        200: serializers.VerifyURLSerializer})
    def post(self, request):
        """ Accept post request for reset users password """
        serializer = serializers.ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_method = serializer.validated_data.get('login_method')
        phone_or_email = is_phone_or_email(login_method)
        otp = otp_generator
        cache_otp(login_method, otp)
        user = get_user_model().objects.get(Q(email=login_method) |
                                            Q(phone_number=login_method))
        if phone_or_email == "email":
            send_otp_email.delay(login_method, otp)
        elif phone_or_email == "phone":
            send_otp_mobile.delay(login_method, otp)
        url = one_time_token_generator.make_token(user)
        return Response(data=serializers.VerifyURLSerializer(
            {'url': url}
        ), status=status.HTTP_201_CREATED)


class ResetPasswordVerify(APIView):
    """ An APIView for verifying users password reset
        its verifying users otp code and password
        then it will set a new password for user
    """

    permission_classes = (AllowAny, )

    @extend_schema(request=serializers.ResetPasswordVerifySerializer, responses={
        200: serializers.UserSerializer,
        403: EmptySerializer
    }, parameters=ONE_TIME_LINK_API_PARAMETERS)
    def post(self, request, uidb64, token):
        """ Accept post request for verifying users password reset """
        serializer = serializers.ResetPasswordVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password_confirm')
        user = one_time_token_generator.decode_token(uidb64)
        if user and one_time_token_generator.check_token(token):
            user.set_password(password)
            user.save()
            return Response(data=serializers.UserSerializer, status=status.HTTP_200_OK)
        return Response(data=serializers.TokenExpiredErrorSerializer(
            {'token': 'Url activation token has been expired'}
        ), status=status.HTTP_403_FORBIDDEN)


class Logout(APIView):
    """ An APIView for logging users out """

    permission_classes = (IsAuthenticated, )

    @extend_schema(request=EmptySerializer, responses={
        205: EmptySerializer, 400: EmptySerializer})
    def post(self, request):
        """ Accept post request for logging out
            set user token to blacklist
        """
        try:
            refresh_token = request.data["refresh_token"]
            AUTH.set_blacklist_token(refresh_token)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
