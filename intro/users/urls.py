from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import apis


urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', apis.Login.as_view(), name="login"),
    path('register/', apis.Register.as_view(), name="register"),
    path('register/verify/<uidb64>/<token>/',
         apis.VerifyRegsiter.as_view()),
    path('logout/', apis.Logout.as_view(), name="logout"),
    path('change/password/',
         apis.ChangePassword.as_view(), name="change_password"),
    path('reset/password/',
         apis.ResetPassword.as_view(), name="reset_password"),
    path('reset/password/verify/<uidb64>/<token>/',
         apis.ResetPasswordVerify.as_view(), name="reset_password_verify")
]
