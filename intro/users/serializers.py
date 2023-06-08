from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from intro.core.cache import get_cached_otp

from intro.utils import validators
from intro.utils.regexes import is_phone_or_email


class BaseAuthSerializer(serializers.Serializer):
    """ The base of all Auth serializers
        that contains login_method for both
        email/phone authentications
    """

    login_method = serializers.CharField()

    def validate_login_method(self, login_method):
        """ custom validator for login_method
            raise ValidationError when login_method
            is not email and phone number
        """
        if not is_phone_or_email(login_method):
            raise serializers.ValidationError("Email or Phone number is not correct!")
        return login_method


class LoginSerializer(BaseAuthSerializer):
    """ Serializer for login API """

    password = serializers.CharField()


class RegisterSerializer(BaseAuthSerializer):
    """ Serializer for Register API """

    registration_type = serializers.ChoiceField(choices=['E', 'P'])
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate_password(self, password):
        """ A function for validating password
            with default django password validation
        """
        validate_password(password=password)
        return password

    def validate(self, validated_data):
        """ custom validation error for passwords
            raising validation error when passwords
            are not match
        """
        if validators.check_user_existence(login_method=validated_data.get('login_method')):
            raise serializers.ValidationError('User is already exist')

        validators.password_match_checker(
            validated_data.get('password'),
            validated_data.get('password_confirm')
        )
        return validated_data


class ResetPasswordSerializer(BaseAuthSerializer):
    """ Serializer for reset users password """
    ...

    def validate(self, validated_data):
        """ Checking and raise Error if User dosent exist
            used for validation on sending otp email
        """
        if not validators.check_user_existence(
            login_method=validated_data.get('login_method')
        ):
            raise serializers.ValidationError('User not found')
        return validated_data


class RegisterVerifySerializer(serializers.Serializer):
    """ Serializer for Verifying registration API """

    code = serializers.CharField(validators=[validators.OTPCodeValidator])

    def validate(self, validated_data):
        """ custom validation error for code
            raise validaiton error when code
            is expired or not valid
        """
        user = self.context['user']
        if user.registration_type == "E":
            login_method = user.email
        else:
            login_method = user.phone_number

        code = int(validated_data.get('code'))
        cached_otp = get_cached_otp(login_method)

        if not cached_otp:
            raise serializers.ValidationError("Code has been expired")
        if code != cached_otp:
            raise serializers.ValidationError("Code is invalid")

        return validated_data


class ResetPasswordVerifySerializer(serializers.Serializer):
    """ Serializer for verifying users password reset """

    code = serializers.CharField(validators=[validators.OTPCodeValidator])
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate_password(self, password):
        """ A function for validating password
            with default django password validation
        """
        validate_password(password=password)
        return password

    def validate(self, validated_data):
        """ custom validation error for code
            raise validaiton error when code
            is expired or not valid
            and checking password matching
        """
        user = self.context['user']
        if user.registration_type == "E":
            login_method = user.email
        else:
            login_method = user.phone_number

        code = int(validated_data.get('code'))
        cached_otp = get_cached_otp(login_method)

        if not cached_otp:
            raise serializers.ValidationError("Code has been expired")
        if code != cached_otp:
            raise serializers.ValidationError("Code is invalid")

        validators.password_match_checker(
            validated_data.get('password'),
            validated_data.get('password_confirm')
        )
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    """ Serializer for changing password API """

    old_password = serializers.CharField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate_old_password(self, old_password):
        """ custom validation for checking
            user old password, raise validation
            error when old password is wrong
        """
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError('The old password is wrong!')
        return old_password

    def validate_password(self, password):
        """ A function for validating password
            with default django password validation
        """
        validate_password(password=password)
        return password

    def validate(self, validated_data):
        """ custom validation error for passwords
            raising validation error when passwords
            are not match
        """
        validators.password_match_checker(
            validated_data.get('password'),
            validated_data.get('password_confirm')
        )
        return validated_data


class TokenSerializer(serializers.Serializer):
    """ Serializer for Response token
        to user at Login API
    """

    refresh = serializers.CharField()
    access = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    """ Refresh token serializer for
        getting refresh token from frontend
        and set it on blacklist on LogoutAPIView
    """
    refresh = serializers.CharField()


class VerifyURLSerializer(serializers.Serializer):
    """ Serializer for response Url to user """

    url = serializers.URLField()


class ErrorSerializer(serializers.Serializer):
    """ Serializer for response error to user """

    error = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """ User serializer for response
        or do any operation to user
    """

    class Meta:
        model = get_user_model()
        fields = [
            "phone_number",
            "email",
            "about",
            "is_active",
        ]
