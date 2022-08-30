from typing import Any, Dict

from rest_framework import serializers
from rest_framework_simplejwt.tokens import UntypedToken


class LoginSerializer(serializers.Serializer[Any]):
    access_token = serializers.CharField(help_text="Google OAuth2 Access Token")


class AuthPayloadSerializer(serializers.Serializer[Any]):
    access = serializers.CharField()
    refresh = serializers.CharField()


class AuthVerifySerializer(serializers.Serializer["Any"]):
    token = serializers.CharField()

    def validate(self, attrs: Dict[str, Any]) -> Any:
        token = UntypedToken(attrs["token"])

        return token.payload


class TokenPayloadSerializer(serializers.Serializer[Any]):
    token_type = serializers.CharField()
    exp = serializers.IntegerField()
    jti = serializers.CharField()
    user_id = serializers.UUIDField()
