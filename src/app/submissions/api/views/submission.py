from django.db.models import QuerySet
from rest_framework import mixins, parsers, viewsets

from app.submissions.api.serializers import SubmissionSerializer
from app.submissions.models import Submission
from utils.rest_framework import BaseViewMixin


class SubmissionViewSet(
    BaseViewMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    parser_classes = (parsers.MultiPartParser,)

    def get_queryset(self) -> QuerySet[Submission]:
        return super().get_queryset().filter(user=self.request.user)
