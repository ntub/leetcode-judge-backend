from rest_framework import serializers

from app.problems.models import Language


class LanguageSerializer(serializers.ModelSerializer[Language]):
    class Meta:
        model = Language
        fields = (
            "name",
            "slug",
            "status",
            "activate_date",
            "deactivate_date",
        )
        read_only_fields = (
            "name",
            "slug",
            "status",
            "activate_date",
            "deactivate_date",
        )
