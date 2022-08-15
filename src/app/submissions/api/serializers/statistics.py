from rest_framework import serializers


class SubmissionStatisticsSerializer(
    serializers.Serializer,
):
    difficulty = serializers.CharField(
        source="question__difficulty",
        read_only=True,
    )
    status = serializers.CharField(
        source="verify_status",
        read_only=True,
    )
    count = serializers.IntegerField(
        source="question_count",
        read_only=True,
    )
