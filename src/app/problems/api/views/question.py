from typing import Type

from rest_framework import viewsets
from rest_framework.serializers import BaseSerializer

from app.problems.api.serializers import QuestionDetailSerializer, QuestionSerializer
from app.problems.models import Question
from utils.rest_framework import BaseViewMixin


class QuestionViewSet(BaseViewMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = "title_slug"
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    action_serializer_mapping = {
        "list": QuestionSerializer,
    }

    def get_serializer_class(self) -> Type[BaseSerializer[Question]]:
        if self.action in self.action_serializer_mapping:
            return self.action_serializer_mapping[self.action]

        return super().get_serializer_class()
