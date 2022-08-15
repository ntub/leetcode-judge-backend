from typing import Type

from django.db.models import QuerySet
from rest_framework import mixins, parsers, viewsets
from rest_framework.serializers import BaseSerializer

from app.submissions.api.serializers import (
    SubmissionSerializer,
    UpdateSubmissionSerializer,
)
from app.submissions.models import Submission
from utils.rest_framework import BaseViewMixin, PageNumberPagination


class SubmissionViewSet(
    BaseViewMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    parser_classes = (parsers.MultiPartParser,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self) -> Type[BaseSerializer[Submission]]:
        if self.action in {"update", "partial_update"}:
            return UpdateSubmissionSerializer
        return super().get_serializer_class()

    def get_queryset(self) -> QuerySet[Submission]:
        return super().get_queryset().filter(user=self.request.user)
