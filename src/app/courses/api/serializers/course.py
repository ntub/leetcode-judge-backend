from django.db import models
from rest_framework import serializers

from app.courses.models import Course
from app.problems.api.serializers import LanguageSerializer, QuestionSerializer
from app.users.api.serializers import SimpleUserSerializer


class CourseSerializer(serializers.ModelSerializer[Course]):
    languages = LanguageSerializer(many=True)
    creator = SimpleUserSerializer()
    updater = SimpleUserSerializer()

    class Meta:
        model = Course
        fields = (
            "id",
            "code",
            "languages",
            "title",
            "description",
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
            "code",
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
        queryset: models.QuerySet[Course],
    ) -> models.QuerySet[Course]:
        return queryset.select_related(
            "creator",
            "updater",
        ).prefetch_related("languages")


class CourseDetailSerializer(serializers.ModelSerializer[Course]):
    questions = QuestionSerializer(many=True)
    users = SimpleUserSerializer(many=True)
    languages = LanguageSerializer(many=True)
    creator = SimpleUserSerializer()
    updater = SimpleUserSerializer()

    class Meta:
        model = Course
        fields = (
            "code",
            "questions",
            "users",
            "languages",
            "title",
            "description",
            "status",
            "activate_date",
            "deactivate_date",
            "created",
            "modified",
            "creator",
            "updater",
        )
        read_only_fields = (
            "code",
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
        queryset: models.QuerySet[Course],
    ) -> models.QuerySet[Course]:
        return queryset.select_related("creator", "updater").prefetch_related(
            "questions",
            "users",
            "languages",
        )
