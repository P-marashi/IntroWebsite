from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator
)

from rest_framework import serializers

from core.cache import get_cached_otp

from utils.validators import password_match_checker, OTPCodeValidator
from utils.regexes import is_phone_or_email


class BaseAuthSerializer(serializers.Serializer):
    login_method = serializers.CharField()

    def validate_login_method(self, validated_data):
        if not is_phone_or_email(validated_data.get("login_method")):
            raise serializers.ValidationError("Email or Phone number is not correct!")
        return validated_data


class LoginSerializer(BaseAuthSerializer):
    password = serializers.CharField()


class RegisterSerializer(BaseAuthSerializer):
    password = serializers.CharField(validators=[
        UserAttributeSimilarityValidator,
        MinimumLengthValidator,
        CommonPasswordValidator,
        NumericPasswordValidator,
    ])
    password_confirm = serializers.CharField()

    def validate_password(self, validated_data):
        password_match_checker(
            validated_data.get('password'),
            validated_data.get('password_confirm')
        )
        return validated_data


class ResetPasswordSerializer(BaseAuthSerializer):
    ...


class ResetPasswordVerifySerializer(serializers.Serializer):
    code = serializers.CharField(validators=[OTPCodeValidator])
    password = serializers.CharField(validators=[
        UserAttributeSimilarityValidator,
        MinimumLengthValidator,
        CommonPasswordValidator,
        NumericPasswordValidator,
    ])
    password_confirm = serializers.CharField()

    def validate_code(self, validated_data):
        login_method = validated_data.get('login_method')
        code = validated_data.get('code')
        cached_otp = get_cached_otp(login_method)
        if not cached_otp:
            if code != cached_otp:
                raise serializers.ValidationError("Code is invalid")
            raise serializers.ValidationError("code has been expired")
        return validated_data

    def validate_password(self, validated_data):
        password_match_checker(
            validated_data.get('password'),
            validated_data.get('password_confirm')
        )
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField(validators=[
        UserAttributeSimilarityValidator,
        MinimumLengthValidator,
        CommonPasswordValidator,
        NumericPasswordValidator,
    ])
    password_confirm = serializers.CharField()

    def validate_old_password(self, validated_data):
        user = self.context['request'].user
        if not user.check_password(validated_data.get('old_password')):
            raise serializers.ValidationError('The old password is wrong!')

    def validate_password(self, validated_data):
        password_match_checker(
            validated_data.get('password'),
            validated_data.get('password_confirm')
        )
        return validated_data


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class VerifyURLSerializer(serializers.Serializer):
    url = serializers.URLField()


class VerifyRegisterSerializer(BaseAuthSerializer):
    code = serializers.CharField(validators=[OTPCodeValidator])

    def validate_code(self, validated_data):
        login_method = validated_data.get('login_method')
        code = validated_data.get('code')
        cached_otp = get_cached_otp(login_method)
        if not cached_otp:
            if code != cached_otp:
                raise serializers.ValidationError("Code is invalid")
            raise serializers.ValidationError("Code has been expired")
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "phone_number",
            "email",
            "about",
            "is_active",
        ]


class TokenExpiredErrorSerializer(serializers.Serializer):
    token = serializers.CharField()


class EmptySerializer(serializers.Serializer):
    ...
