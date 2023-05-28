from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework_simplejwt.tokens import RefreshToken


class EmailOrPhoneNumberAuthentication:
    """ Custom Backend for both email and phone_number """
    
    @staticmethod
    def authenticate(email: str = None,
                     phone_number: str = None, password: str = None):
        """
        check user login method and password
        """
        try:
            user = get_user_model().objects.get(
                Q(phone_number=phone_number) | Q(email=email)
            )
        except get_user_model().DoesNotExist:
            return None

        if user and user.check_password(password):
            return user

        return None

    @staticmethod
    def generate_token(user):
        """ Generate jwt token for given user """
        return RefreshToken.for_user(user)

    @staticmethod
    def set_blacklist_token(refresh_token):
        """ Set given token into blacklist """
        token = RefreshToken(refresh_token)
        return token.blacklist()


# declare variable to our custom backend for easy access to it
AUTH = EmailOrPhoneNumberAuthentication()
