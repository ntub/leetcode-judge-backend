from rest_framework import permissions, viewsets

from app.bulletins.api.serializers import AnnouncementSerializer
from app.bulletins.models import Announcement
from utils.rest_framework import BaseViewMixin


class AnnouncementViewSet(BaseViewMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.active()  # type: ignore
    serializer_class = AnnouncementSerializer
    permission_classes = (permissions.AllowAny,)
