from django.db import models
from rest_framework import serializers

from app.bulletins.models import Announcement
from app.courses.api.serializers import CourseSerializer
from app.users.api.serializers import SimpleUserSerializer


class AnnouncementSerializer(serializers.ModelSerializer[Announcement]):
    courses = CourseSerializer(many=True)
    creator = SimpleUserSerializer()
    updater = SimpleUserSerializer()

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "description",
            "courses",
            "status",
            "activate_date",
            "deactivate_date",
            "created",
            "modified",
            "creator",
            "updater",
        )
        read_only_fields = (
            "id",
            "status",
            "activate_date",
            "deactivate_date",
            "created",
            "modified",
            "creator",
            "updater",
        )

    @staticmethod
    def setup_eager_loading(
        queryset: models.QuerySet[Announcement],
    ) -> models.QuerySet[Announcement]:
        return queryset.select_related(
            "creator",
            "updater",
        ).prefetch_related("courses")
