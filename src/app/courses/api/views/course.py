from typing import Type

from django.db.models import QuerySet
from rest_framework import filters, viewsets
from rest_framework.serializers import BaseSerializer

from app.courses.api.serializers import CourseDetailSerializer, CourseSerializer
from app.courses.models import Course
from utils.rest_framework import BaseViewMixin, PageNumberPagination
from utils.rest_framework.filters import SearchFilter


class CourseViewSet(BaseViewMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = "code"
    queryset = Course.objects.active()
    serializer_class = CourseDetailSerializer
    pagination_class = PageNumberPagination
    action_serializer_mapping = {
        "list": CourseSerializer,
    }
    filter_backends = (
        filters.OrderingFilter,
        SearchFilter,
    )
    search_fields = ("title", "code")

    def get_queryset(self) -> QuerySet[Course]:
        return super().get_queryset().filter(users=self.request.user)

    def get_serializer_class(self) -> Type[BaseSerializer[Course]]:
        if self.action in self.action_serializer_mapping:
            return self.action_serializer_mapping[self.action]

        return super().get_serializer_class()
