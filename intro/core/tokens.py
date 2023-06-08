import six

from django.contrib.auth import get_user_model
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class OneTimeTokenGenerator(PasswordResetTokenGenerator):
    """ Generate a one-time activation hash token
        by inherit of PasswordResetTokenGenerator
    """

    def create_url_activation(self, user):
        """ Create a one time activation token
        ...
        Params:
        -------
        user -> User object

        Returns:
        --------
        str -> path of <uid>/<token>
        """
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = self.make_token(user)
        return f"{uid}/{token}"

    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        """ creating a hashed token by given user and timestamp """
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

    def check_url_token(self, uidb64, token):
        """ decode hashed token
        ...
        Params:
        -------
        uidb64 -> str
        token -> str

        Returns:
        --------
        User Object | False (If token was expired)
        """
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        if self.check_token(user=user, token=token):
            return user
        return False


# declaring its variable to access it easily in everywhere of project
one_time_token_generator = OneTimeTokenGenerator()
