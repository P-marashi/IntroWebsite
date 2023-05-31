import six

from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class OneTimeTokenGenerator(PasswordResetTokenGenerator):
    """ Generate a one-time activation hash token
        by inherit of PasswordResetTokenGenerator
    """

    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        """ creating a hashed token by given user and timestamp """
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

    def decode_token(self, uidb64):
        """ decode hashed token """
        uid = force_str(urlsafe_base64_decode(uidb64))
        # user = get_user_model().objects.get(pk=uid)
        # return user


# declaring its variable to access it easily in everywhere of project
one_time_token_generator = OneTimeTokenGenerator()
