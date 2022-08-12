from typing import Type

from rest_framework import filters, viewsets
from rest_framework.serializers import BaseSerializer

from app.problems.api.serializers import QuestionDetailSerializer, QuestionSerializer
from app.problems.models import Question
from utils.rest_framework import BaseViewMixin, PageNumberPagination
from utils.rest_framework.filters import SearchFilter


class QuestionViewSet(BaseViewMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = "title_slug"
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    pagination_class = PageNumberPagination
    action_serializer_mapping = {
        "list": QuestionSerializer,
    }
    filter_backends = (
        filters.OrderingFilter,
        SearchFilter,
    )
    search_fields = ("title", "code")

    def get_serializer_class(self) -> Type[BaseSerializer[Question]]:
        if self.action in self.action_serializer_mapping:
            return self.action_serializer_mapping[self.action]

        return super().get_serializer_class()
