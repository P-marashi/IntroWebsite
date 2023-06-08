from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers


class OTPCodeValidator:
    """ Custom Validation for One-Time-Pin code
    Numerical
    Minimum Length is: 5
    Maximum Length is: 5
    """
    message = "%(code) code should be numeric with 5 length"

    def __init__(self, message=None):
        self.message = message or self.message

    def __call__(self, attrs):
        self.code = attrs['code']
        code = str(self.code)
        if not len(code) == 5 and isinstance(attrs['code'], int):
            raise serializers.ValidationError(self.message % (code), code="otp_invalid")

    def __repr__(self):
        return "<%s(code=%s)>" % (self.__class__.__name__, self.code)


def password_match_checker(password, password_confirm):
    """ password similarity checker
        raise Validation error when passwords arent match
    ...
    ARGS:
    -----
    password: str
    password_confirm: str

    Returns:
    --------
    bool: True

    Raise:
    ------
    serializers.ValidationError Exception
    """
    if password != password_confirm:
        raise serializers.ValidationError("Passwords arent match")
    return 1


def check_user_existence(login_method):
    try:
        user = get_user_model().objects.values("is_active").get(
            Q(email=login_method) |
            Q(phone_number=login_method)
        )
        if user['is_active']:
            return 1
        return 0
    except get_user_model().DoesNotExist:
        return 0
