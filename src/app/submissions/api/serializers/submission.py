from typing import Any, OrderedDict

from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.courses.api.serializers import CourseSerializer
from app.courses.models import Course
from app.problems.api.serializers import LanguageSerializer, QuestionSerializer
from app.problems.models import Language, Question
from app.submissions.models import Submission
from app.users.api.serializers import SimpleUserSerializer


class SubmissionSerializer(serializers.ModelSerializer[Submission]):
    question_title_slug = serializers.SlugRelatedField(
        source="question",
        slug_field="title_slug",
        queryset=Question.objects.all(),
    )
    lang_slug = serializers.SlugRelatedField(
        source="lang",
        slug_field="slug",
        queryset=Language.objects.active(),
    )
    course_code = serializers.SlugRelatedField(
        source="course",
        slug_field="code",
        queryset=Course.objects.active(),
        allow_null=True,
        required=False,
    )
    user = SimpleUserSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)
    lang = LanguageSerializer(read_only=True)
    course = CourseSerializer(allow_null=True, read_only=True)
    verifier = SimpleUserSerializer(allow_null=True, read_only=True)
    creator = SimpleUserSerializer(read_only=True)
    updater = SimpleUserSerializer(read_only=True)

    def validate(
        self,
        attrs: OrderedDict[str, Any],
    ) -> OrderedDict[str, Any]:
        attrs = super().validate(attrs)
        user = self.context["request"].user
        attrs["user"] = user
        question = attrs["question"]  # type: Question
        lang = attrs["lang"]  # type: Language
        course = attrs.get("course")
        if not question.code_snippets.filter(
            lang_slug=lang.slug,
        ).exists():
            raise serializers.ValidationError(
                {"question": _("`lang` not in Question")},
            )

        if course:  # type: Course
            users = list(course.users.all())
            if users and user not in users:
                raise serializers.ValidationError(
                    {"course": _("`user` not in Course.")},
                )

            questions = list(course.questions.all())
            if questions and question not in questions:
                raise serializers.ValidationError(
                    {"course": _("`question` not in Course.")},
                )

            languages = list(course.languages.all())
            if languages and lang not in languages:
                raise serializers.ValidationError(
                    {"course": _("`lang` not in Course.")},
                )

        return attrs

    class Meta:
        model = Submission
        fields = (
            "id",
            "user",
            "question",
            "lang",
            "source_code",
            "solved",
            "snapshot",
            "course",
            "runtime",
            "memory",
            "runtime_rating",
            "memory_rating",
            "difficulty",
            "verify_status",
            "verifier",
            "verified",
            "created",
            "modified",
            "creator",
            "updater",
            "question_title_slug",
            "lang_slug",
            "course_code",
        )
        read_only_fields = (
            "id",
            "user",
            "question",
            "lang",
            "course",
            "verify_status",
            "verifier",
            "verified",
            "created",
            "modified",
            "creator",
            "updater",
        )

    @staticmethod
    def setup_eager_loading(
        queryset: models.QuerySet[Submission],
    ) -> models.QuerySet[Submission]:
        return queryset.select_related(
            "user",
            "question",
            "lang",
            "course",
            "verifier",
            "creator",
            "updater",
        )
