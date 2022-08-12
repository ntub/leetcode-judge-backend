from rest_framework import filters, permissions, viewsets

from app.bulletins.api.serializers import AnnouncementSerializer
from app.bulletins.models import Announcement
from utils.rest_framework import BaseViewMixin
from utils.rest_framework.filters import SearchFilter


class AnnouncementViewSet(BaseViewMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.active()  # type: ignore
    serializer_class = AnnouncementSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (
        filters.OrderingFilter,
        SearchFilter,
    )
    search_fields = ("title",)
