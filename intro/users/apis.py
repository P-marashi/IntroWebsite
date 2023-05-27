from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from utils.regexes import is_phone_or_email
from utils.otp import otp_generator

from core.tokens import one_time_token_generator
from core.cache import cache_otp
from core.tasks import send_otp_email, send_otp_mobile

from .serializers import (
    LoginSerializer,
    TokenSerializer,
    RegisterSerializer,
    VerifyURLSerializer,
    VerifyRegisterSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    TokenExpiredErrorSerializer,
    ResetPasswordSerializer,
    ResetPasswordVerifySerializer,
    EmptySerializer
)
from .backends import EmailOrPhoneNumberAuthentication as Authenticate


AUTH = Authenticate()


class Login(APIView):
    @extend_schema(request=LoginSerializer, responses={200: TokenSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_method = serializer.validated_data.get('login_method')
        password = serializer.validated_data.get('password')
        user = AUTH.authenticate(request, is_phone_or_email(login_method),
                                 password=password)
        tokens = AUTH.generate_token(user)
        return Response(data=TokenSerializer(tokens),
                        status=status.HTTP_200_OK)


class Register(APIView):
    @extend_schema(request=RegisterSerializer, responses={
        201: VerifyURLSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
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
        return Response(data=VerifyURLSerializer(
            {'url': url}
        ), status=status.HTTP_201_CREATED)


class VerifyRegsiter(APIView):
    @extend_schema(request=VerifyRegisterSerializer, responses={
        200: UserSerializer,
        403: TokenExpiredErrorSerializer})
    def post(self, request, uidb64, token):
        user = one_time_token_generator.decode_token(uidb64)
        if user and one_time_token_generator.check_token(token):
            serializer = VerifyRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            login_method = serializer.validated_data.get('login_method')
            user = get_user_model().objects.get(
                Q(email=login_method) | Q(phone_number=login_method)
            )
            user.is_active = True
            user.save()
            return Response(data=UserSerializer(user),
                            status=status.HTTP_200_OK)
        return Response(data=TokenExpiredErrorSerializer({
            'token': 'Url activation token is expired.'
        }), status=status.HTTP_403_FORBIDDEN)


class ChangePassword(APIView):
    @extend_schema(request=ChangePasswordSerializer, responses={
        200: UserSerializer})
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password_confirm')
        request.user.set_password(password)
        request.user.save()
        return Response(data=UserSerializer(request.user),
                        status=status.HTTP_200_OK)


class ResetPassword(APIView):
    @extend_schema(request=ResetPasswordSerializer, responses={
        200: VerifyURLSerializer})
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
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
        return Response(data=VerifyURLSerializer(
            {'url': url}
        ), status=status.HTTP_201_CREATED)


class ResetPasswordVerify(APIView):
    @extend_schema(request=ResetPasswordVerifySerializer, responses={
        200: UserSerializer,
        403: EmptySerializer
    })
    def post(self, request, uidb64, token):
        serializer = ResetPasswordVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password_confirm')
        user = one_time_token_generator.decode_token(uidb64)
        if user and one_time_token_generator.check_token(token):
            user.set_password(password)
            user.save()
            return Response(data=UserSerializer, status=status.HTTP_200_OK)
        return Response(data=TokenExpiredErrorSerializer(
            {'token': 'Url activation token has been expired'}
        ), status=status.HTTP_403_FORBIDDEN)


class Logout(APIView):
    @extend_schema(request=EmptySerializer, responses={
        205: EmptySerializer, 400: EmptySerializer})
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            AUTH.set_blacklist_token(refresh_token)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
