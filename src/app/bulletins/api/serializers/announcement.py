from django.db import models
from rest_framework import serializers

from app.bulletins.models import Announcement, AttachFile
from app.courses.api.serializers import CourseSerializer
from app.users.api.serializers import SimpleUserSerializer
from utils.rest_framework import build_model_serializer


class AnnouncementSerializer(serializers.ModelSerializer[Announcement]):
    courses = CourseSerializer(many=True)
    creator = SimpleUserSerializer()
    updater = SimpleUserSerializer()
    attach_files = build_model_serializer(
        AttachFile,
        field_list=["file", "name"],
        read_only_list=["file", "name"],
        many=True,
        read_only=True,
    )

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "description",
            "courses",
            "attach_files",
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
            "attach_files",
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
        ).prefetch_related("courses", "attach_files")
