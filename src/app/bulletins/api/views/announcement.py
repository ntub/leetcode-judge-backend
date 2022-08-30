from rest_framework import filters, permissions, viewsets

from app.bulletins.api.serializers import AnnouncementSerializer
from app.bulletins.models import Announcement
from utils.rest_framework import BaseViewMixin, PageNumberPagination
from utils.rest_framework.filters import SearchFilter


class AnnouncementViewSet(BaseViewMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.active()
    serializer_class = AnnouncementSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (
        filters.OrderingFilter,
        SearchFilter,
    )
    search_fields = ("title",)
