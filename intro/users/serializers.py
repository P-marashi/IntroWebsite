from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from intro.core.cache import get_cached_otp

from intro.utils.validators import password_match_checker, OTPCodeValidator
from intro.utils.regexes import is_phone_or_email


class BaseAuthSerializer(serializers.Serializer):
    """ The base of all Auth serializersimport django.contrib.auth.password_validation as validators
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

    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate_password(self, password):
        validate_password(password=password)
        return password

    def validate(self, validated_data):
        """ custom validation error for passwords
            raising validation error when passwords
            are not match
        """
        password_match_checker(
            validated_data.get('password'),
            validated_data.get('password_confirm')
        )
        return validated_data


class RegisterVerifySerializer(BaseAuthSerializer):
    """ Serializer for Verifying registration API """

    code = serializers.CharField(validators=[OTPCodeValidator])

    def validate(self, validated_data):
        """ custom validation error for code
            raise validaiton error when code
            is expired or not valid
        """
        login_method = validated_data.get('login_method')
        code = validated_data.get('code')
        cached_otp = get_cached_otp(login_method)
        if not cached_otp:
            if code != cached_otp:
                raise serializers.ValidationError("Code is invalid")
            raise serializers.ValidationError("Code has been expired")
        return validated_data


class ResetPasswordSerializer(BaseAuthSerializer):
    """ Serializer for reset users password """
    ...


class ResetPasswordVerifySerializer(serializers.Serializer):
    """ Serializer for verifying users password reset """

    code = serializers.CharField(validators=[OTPCodeValidator])
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate_password(self, password):
        return validate_password(password=password)

    def validate(self, validated_data):
        """ custom validation error for code
            raise validaiton error when code
            is expired or not valid
        """
        login_method = validated_data.get('login_method')
        code = validated_data.get('code')
        cached_otp = get_cached_otp(login_method)
        if not cached_otp:
            if code != cached_otp:
                raise serializers.ValidationError("Code is invalid")
            raise serializers.ValidationError("code has been expired")
        return validated_data

    def validate_password(self, validated_data):
        """ custom validation error for passwords
            raising validation error when passwords
            are not match
        """
        password_match_checker(
            validated_data.get('password'),
            validated_data.get('password_confirm')
        )
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    """ Serializer for changing password API """

    old_password = serializers.CharField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate_password(self, password):
        return validate_password(password=password)

    def validate_old_password(self, validated_data):
        """ custom validation for checking
            user old password, raise validation
            error when old password is wrong
        """
        user = self.context['request'].user
        if not user.check_password(validated_data.get('old_password')):
            raise serializers.ValidationError('The old password is wrong!')
        return validated_data

    def validate_password(self, validated_data):
        """ custom validation error for passwords
            raising validation error when passwords
            are not match
        """
        password_match_checker(
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
