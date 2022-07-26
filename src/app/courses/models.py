from functools import partial

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import ActivatorModelManager, TitleDescriptionModel

from app.courses.utils import generate_serial_number
from app.problems.models import Language, Question
from app.users.models import User
from utils.django.managers import BaseManager
from utils.django.models import BaseActivatorModel


class CourseManager(
    ActivatorModelManager,  # type: ignore
    BaseManager["Course"],
):
    pass


class Course(BaseActivatorModel, TitleDescriptionModel):  # type: ignore
    code = models.CharField(
        _("code"),
        max_length=10,
        default=partial(
            generate_serial_number,
            "courses.Course",
            "C",
            "code",
        ),
        unique=True,
    )
    # Blank is allow questions.
    questions = models.ManyToManyField(
        Question,
        verbose_name=_("questions"),
        related_name="courses",
        blank=True,
    )
    # Blank is allow anyone.
    users = models.ManyToManyField(
        User,
        verbose_name=_("users"),
        related_name="courses",
        blank=True,
    )
    # Blank is allow languages.
    languages = models.ManyToManyField(
        Language,
        verbose_name=_("languages"),
        related_name="courses",
        blank=True,
    )
    objects = CourseManager()

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")
