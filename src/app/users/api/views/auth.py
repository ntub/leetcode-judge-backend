from typing import Any, Type

from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.exceptions import AuthForbidden
from social_django.utils import load_backend, load_strategy

from app.users.api.serializers import (
    AuthPayloadSerializer,
    AuthVerifySerializer,
    LoginSerializer,
    TokenPayloadSerializer,
)


class AuthViewSet(viewsets.GenericViewSet):
    """
    Social Auth View Set.

    ref: https://pastebin.com/08iLNCJc
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    pagination_class = None

    def get_serializer_class(self) -> Type[serializers.BaseSerializer[Any]]:
        if self.action == "refresh":
            return TokenRefreshSerializer  # type: ignore
        elif self.action == "verify":
            return AuthVerifySerializer
        return super().get_serializer_class()

    @swagger_auto_schema(responses={200: AuthPayloadSerializer})  # type: ignore
    @action(["post"], detail=False)
    def login(self, request: Request) -> Response:
        """
        Login and validate.

        - Args
        access_token: str Google OAuth2 Auth access token.
        `OAuth2 scopes: 'profile email'`.


        - Returns
        access: str
        refresh: str

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        strategy = load_strategy(request=request)
        backend = load_backend(strategy, "google-oauth2", redirect_uri=None)
        access_token = serializer.data.get("access_token")
        try:
            user = backend.do_auth(access_token)
            # user = backend.do_auth(access_token, user=user)
        except AuthForbidden:
            raise AuthenticationFailed("Invalid Token")

        if not user or not user.is_active:
            raise AuthenticationFailed(
                _("No active account found with the given credentials"),
                "no_active_account",
            )
        # login(request, user)
        token = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(token.access_token),
                "refresh": str(token),
            },
        )

    @swagger_auto_schema(responses={200: AuthPayloadSerializer})  # type: ignore
    @action(["post"], detail=False)
    def refresh(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data)

    @swagger_auto_schema(responses={200: TokenPayloadSerializer})  # type: ignore
    @action(["post"], detail=False)
    def verify(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data)
