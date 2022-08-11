from rest_framework import serializers

from app.problems.models import CodeSnippet


class CodeSnippetSerializer(serializers.ModelSerializer[CodeSnippet]):
    class Meta:
        model = CodeSnippet
        fields = (
            "lang",
            "lang_slug",
        )
        read_only_fields = (
            "lang",
            "lang_slug",
        )
