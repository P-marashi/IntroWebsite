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


def password_match_checker(password, passworc_confirm):
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
    if password != passworc_confirm:
        raise serializers.ValidationError("Passwords arent match")
    return 1
