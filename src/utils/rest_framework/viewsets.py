from typing import Callable, TypeVar

from django.db.models import Model, QuerySet
from rest_framework import generics

_MT_co = TypeVar("_MT_co", bound=Model, covariant=True)


class EagerLoadingViewMixin(generics.GenericAPIView):  # type: ignore[type-arg]
    def get_queryset(self) -> QuerySet[_MT_co]:
        setup_eager_loading: Callable[[QuerySet[_MT_co]], QuerySet[_MT_co]] = getattr(
            self.get_serializer_class(),
            "setup_eager_loading",
            lambda qs: qs,
        )

        return setup_eager_loading(super().get_queryset())


class BaseViewMixin(EagerLoadingViewMixin):
    pass
