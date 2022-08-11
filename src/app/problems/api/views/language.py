from rest_framework import viewsets

from app.problems.api.serializers import LanguageSerializer
from app.problems.models import Language
from utils.rest_framework import BaseViewMixin


class LanguageViewSet(BaseViewMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    queryset = Language.objects.active()  # type: ignore
    serializer_class = LanguageSerializer
