from collections import namedtuple

from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from app.submissions.models import Submission
from app.users.api.serializers import UserStatisticsSerializer
from app.users.models import User
from utils.rest_framework import BaseViewMixin


class UserViewSet(BaseViewMixin, viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserStatisticsSerializer
    pagination_class = None
    filter_backends = []

    @action(["get"], detail=False)
    @swagger_auto_schema(
        responses={  # type: ignore
            status.HTTP_200_OK: UserStatisticsSerializer,
        },
    )
    def me(self, request: Request) -> Response:
        user_statistics_class = namedtuple(
            "UserStatistics",
            ["user", "statistics"],
        )
        user_statistics = user_statistics_class(
            user=request.user,
            statistics=Submission.objects.select_related(
                "question",
            )
            .values(
                "question__difficulty",
                "verify_status",
            )
            .annotate(
                question_count=Count("question__difficulty"),
            ),
        )
        serializer = self.get_serializer(user_statistics)
        return Response(serializer.data)
