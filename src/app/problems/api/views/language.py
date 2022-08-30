from rest_framework import filters, viewsets

from app.problems.api.serializers import LanguageSerializer
from app.problems.models import Language
from utils.rest_framework import BaseViewMixin, PageNumberPagination
from utils.rest_framework.filters import SearchFilter


class LanguageViewSet(BaseViewMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    queryset = Language.objects.active()
    serializer_class = LanguageSerializer
    pagination_class = PageNumberPagination
    filter_backends = (
        filters.OrderingFilter,
        SearchFilter,
    )
    search_fields = ("title", "code")
