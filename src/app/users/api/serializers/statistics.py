from rest_framework import serializers

from app.submissions.api.serializers import SubmissionStatisticsSerializer
from app.users.api.serializers.user import UserSerializer


class UserStatisticsSerializer(
    serializers.Serializer,
):
    user = UserSerializer(read_only=True)
    statistics = SubmissionStatisticsSerializer(
        many=True,
        read_only=True,
    )
