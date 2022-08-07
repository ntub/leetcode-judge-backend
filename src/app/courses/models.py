from functools import partial

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TitleDescriptionModel

from app.courses.utils import generate_serial_number
from utils.django.models import BaseActivatorModel


class Course(TitleDescriptionModel, BaseActivatorModel):
    code = models.CharField(
        _("code"),
        max_length=10,
        default=partial(generate_serial_number, "courses.Course", "C", "code"),
    )

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")
