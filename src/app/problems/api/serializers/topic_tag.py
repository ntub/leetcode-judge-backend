from rest_framework import serializers

from app.problems.models import TopicTag


class TopicTagSerializer(serializers.ModelSerializer[TopicTag]):
    class Meta:
        model = TopicTag
        fields = (
            "name",
            "slug",
        )
        read_only_fields = (
            "name",
            "slug",
        )
