from typing import Any, Callable, Dict, Optional, TypeVar, Union

from django.contrib.admin import ModelAdmin
from django.db import models
from django.forms import Form
from django.http import HttpRequest

from utils.django.models import BaseModel

_T = TypeVar("_T", bound=models.Model, covariant=True)


def action_display(
    function: Optional[Callable[[ModelAdmin[_T]], Any]] = None,
    *,
    label: Optional[str] = None,
    description: Optional[str] = None,
    attrs: Optional[Dict[str, Any]] = None,
) -> Any:
    def decorator(func: Any) -> Any:
        if label is not None:
            func.label = label
        if description is not None:
            func.short_description = description
        if attrs is not None:
            func.attrs = attrs
        return func

    if function is None:
        return decorator
    else:
        return decorator(function)


class AuditModelAdmin(ModelAdmin[_T]):
    def save_model(
        self,
        request: HttpRequest,
        obj: Union[models.Model, BaseModel],
        form: Form,
        change: Any,
    ) -> None:
        if hasattr(obj, "creator") and obj._state.adding:
            obj.creator = request.user  # type: ignore

        if hasattr(obj, "updater"):
            obj.updater = request.user  # type: ignore

        super().save_model(request, obj, form, change)  # type: ignore
