from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.serializers import BaseSerializer

from app.courses.api.serializers import CourseDetailSerializer, CourseSerializer
from app.courses.models import Course
from utils.rest_framework import BaseViewMixin


class CourseViewSet(BaseViewMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = "code"
    queryset = Course.objects.active()
    serializer_class = CourseDetailSerializer
    action_serializer_mapping = {
        "list": CourseSerializer,
    }

    def get_queryset(self) -> QuerySet[Course]:
        return super().get_queryset().filter(users=self.request.user)

    def get_serializer_class(self) -> Type[BaseSerializer[Course]]:
        if self.action in self.action_serializer_mapping:
            return self.action_serializer_mapping[self.action]

        return super().get_serializer_class()
