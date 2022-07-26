from typing import TYPE_CHECKING, Any, List, Optional, Type, Union

from django.db import models
from rest_framework import serializers


def build_model_serializer_class(
    model_class: Type[models.Model],
    field_list: Union[str, List[str]] = "__all__",
    read_only_list: Optional[List[str]] = None,
) -> Type[serializers.ModelSerializer[Any]]:
    class SimpleModelSerializer(serializers.ModelSerializer[Any]):
        class Meta:
            model = model_class
            fields = field_list
            read_only_fields = read_only_list or ["id"]

    name = f"Simple{model_class.__name__}Serializer"
    if TYPE_CHECKING:
        serializer_class = SimpleModelSerializer
    else:
        serializer_class = type(
            name,
            (SimpleModelSerializer,),
            dict(),
        )
    return serializer_class


def build_model_serializer(
    model_class: Type[models.Model],
    field_list: Union[str, List[str]] = "__all__",
    read_only_list: Optional[List[str]] = None,
    **kwargs: Any,
) -> serializers.ModelSerializer[Any]:
    serializer = build_model_serializer_class(
        model_class=model_class,
        field_list=field_list,
        read_only_list=read_only_list,
    )
    if kwargs:
        return serializer(**kwargs)

    return serializer()
