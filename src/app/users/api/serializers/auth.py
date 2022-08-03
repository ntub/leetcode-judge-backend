from rest_framework import serializers
from rest_framework_simplejwt.tokens import UntypedToken


class LoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(help_text="Google OAuth2 Access Token")


class AuthPayloadSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class AuthVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = UntypedToken(attrs["token"])

        return token.payload


class TokenPayloadSerializer(serializers.Serializer):
    token_type = serializers.CharField()
    exp = serializers.IntegerField()
    jti = serializers.CharField()
    user_id = serializers.UUIDField()
