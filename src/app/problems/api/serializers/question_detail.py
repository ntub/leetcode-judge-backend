from django.db import models
from rest_framework import serializers

from app.problems.api.serializers.code_snippet import CodeSnippetSerializer
from app.problems.api.serializers.topic_tag import TopicTagSerializer
from app.problems.models import Question


class QuestionDetailSerializer(serializers.ModelSerializer[Question]):
    topic_tags = TopicTagSerializer(many=True)
    code_snippets = CodeSnippetSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            "title",
            "title_slug",
            "content",
            "difficulty",
            "topic_tags",
            "code_snippets",
        )
        read_only_fields = (
            "title",
            "title_slug",
            "topic_tags",
            "code_snippets",
        )

    @staticmethod
    def setup_eager_loading(
        queryset: models.QuerySet[Question],
    ) -> models.QuerySet[Question]:
        return queryset.prefetch_related(
            "topic_tags",
            "code_snippets",
        )
