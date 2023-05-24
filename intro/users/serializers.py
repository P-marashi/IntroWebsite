import re
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator
)
from rest_framework import serializers

from utils.validators import password_match_checker
from utils.regexes import EMAIL_REGEX, PHONE_NUMBER_REGEX


class BaseSerializer(serializers.Serializer):
    login_method = serializers.CharField()

    def validate_login_method(self, validated_data):
        if not re.match(PHONE_NUMBER_REGEX, validated_data.get('login_method')):
            if not re.match(EMAIL_REGEX, validated_data.get('login_method')):
                raise serializers.ValidationError('Ridi Pesar')


class LoginSerializer(BaseSerializer):
    password = serializers.CharField(validators=[
        UserAttributeSimilarityValidator,
        MinimumLengthValidator,
        CommonPasswordValidator,
        NumericPasswordValidator,
    ])


class RegisterSerializer(BaseSerializer):
    ...


class ResetPasswordSerializer(BaseSerializer):
    ...


class ResetPasswordVerifySerializer(serializers.Serializer):
    password = serializers.CharField(validators=[
        UserAttributeSimilarityValidator,
        MinimumLengthValidator,
        CommonPasswordValidator,
        NumericPasswordValidator,
    ])
    password_confirm = serializers.CharField()

    def validate_password(self, validated_data):
        return password_match_checker(
            validated_data.get('password'), 
            validated_data.get('password_confirm')
        )



class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(validators=[
        UserAttributeSimilarityValidator,
        MinimumLengthValidator,
        CommonPasswordValidator,
        NumericPasswordValidator,
    ])
    password_confirm = serializers.CharField()

    def validate_password(self, validated_data):
        return password_match_checker(
            validated_data.get('password'), 
            validated_data.get('password_confirm')
        )
