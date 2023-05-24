from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer


class Login(APIView):
    def post(self, request): ...

class Register(APIView):
    def post(self, request): ...

class VerifyRegsiter(APIView):
    def post(self, request): ...

class ChangePassword(APIView):
    def put(self, request): ...

class ResetPassword(APIView):
    def put(self, request): ...

class ResetPasswordVerify(APIView):
    def post(self, request): ...
