import typing
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import ActivatorModel, TimeStampedModel

from utils.django.managers import BaseManager

__all__ = ["UUIDModel", "BaseModel", "BaseActivatorModel"]

USER_MODEL = settings.AUTH_USER_MODEL


class UUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    objects: models.Manager[typing.Any] = BaseManager()

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, UUIDModel):  # type: ignore
    creator = models.ForeignKey(
        USER_MODEL,
        verbose_name=_("creator"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
        editable=False,
    )
    updater = models.ForeignKey(
        USER_MODEL,
        verbose_name=_("updater"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
        editable=False,
    )

    class Meta:
        abstract = True


class BaseActivatorModel(ActivatorModel, BaseModel):  # type: ignore
    class Meta:
        abstract = True
