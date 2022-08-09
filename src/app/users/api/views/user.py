from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from app.users.api.serializers import UserSerializer
from app.users.models import User
from utils.rest_framework import BaseViewMixin


class UserViewSet(BaseViewMixin, viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    pagination_class = None
    filter_backends = []

    @action(["get"], detail=False)
    @swagger_auto_schema(
        responses={  # type: ignore
            status.HTTP_200_OK: UserSerializer,
        },
    )
    def me(self, request: Request) -> Response:
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
