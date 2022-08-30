from typing import Any, Dict, NamedTuple, Union

from django.contrib.auth.models import AnonymousUser
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from app.problems.models import Question
from app.submissions.models import Submission
from app.users.api.serializers import UserStatisticsSerializer
from app.users.models import User
from utils.rest_framework import BaseViewMixin

_UserStatistics = NamedTuple(
    "_UserStatistics",
    [("user", Union[User, AnonymousUser]), ("statistics", Dict[str, Any])],
)


class UserViewSet(BaseViewMixin, viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserStatisticsSerializer
    pagination_class = None
    filter_backends = []  # type: ignore

    @action(["get"], detail=False)
    @swagger_auto_schema(
        responses={  # type: ignore
            status.HTTP_200_OK: UserStatisticsSerializer,
        },
    )
    def me(self, request: Request) -> Response:
        statistics_values = list(
            Submission.objects.select_related(
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
        status_list = Submission.VerifyStatus.values
        difficulty_list = list(
            Question.objects.distinct().values_list("difficulty", flat=True),
        )
        statistics_mapping = {}
        stat_key_fmt = "%s__%s"
        # Initial
        for difficulty_ in difficulty_list:
            for status_ in status_list:
                stat_key = stat_key_fmt % (difficulty_, status_)
                statistics_mapping[stat_key] = {
                    "question__difficulty": difficulty_,
                    "verify_status": status_,
                    "question_count": 0,
                }

        for user_stat in statistics_values:
            difficulty_ = user_stat["question__difficulty"]
            status_ = user_stat["verify_status"]
            stat_key = stat_key_fmt % (difficulty_, status_)
            statistics_mapping[stat_key] = user_stat

        user_statistics = _UserStatistics(
            user=request.user,
            statistics=statistics_mapping.values(),  # type: ignore
        )
        serializer = self.get_serializer(user_statistics)
        return Response(serializer.data)
