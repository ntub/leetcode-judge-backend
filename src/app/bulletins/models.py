import os

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TitleDescriptionModel

from app.courses.models import Course
from utils.django.models import BaseActivatorModel, BaseModel


class Announcement(TitleDescriptionModel, BaseActivatorModel):
    description = RichTextUploadingField(
        verbose_name=_("description"),
        config_name="default",
    )
    courses = models.ManyToManyField(
        Course,
        verbose_name=_("courses"),
        related_name="announcements",
        blank=True,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("announcement")
        verbose_name_plural = _("announcements")


def file_path(instance: "AttachFile", filename: str) -> str:
    folder = str(instance.pk).lower().replace("-", "")
    filename = filename.lower().replace("-", "")
    return f"attach_files/{folder}/{filename}"


class AttachFile(BaseModel):
    file = models.FileField(_("file"), upload_to=file_path)
    announcement = models.ForeignKey(
        Announcement,
        verbose_name=_("announcement"),
        related_name="attach_files",
        on_delete=models.CASCADE,
    )

    @property
    def name(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = _("attach file")
        verbose_name_plural = _("attach files")
