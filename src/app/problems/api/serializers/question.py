from rest_framework import serializers

from app.problems.models import Question


class QuestionSerializer(serializers.ModelSerializer[Question]):
    class Meta:
        model = Question
        fields = (
            "title",
            "title_slug",
            "difficulty",
        )
        read_only_fields = (
            "title",
            "title_slug",
        )
