from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.courses.models import Course
from app.problems.models import Language, Question
from app.users.models import User
from utils.django.models import BaseModel


def snapshot_upload_path(instance: "Submission", filename: str) -> str:
    question_slug = instance.question.title_slug.replace("-", "_")
    username = instance.user.username
    id = str(instance.id).replace("-", "")
    return f"submission_snapshots/{question_slug}/{username}/{id}{filename}"


class Submission(BaseModel):
    class VerifyStatus(models.TextChoices):
        ACCEPTED = "accepted", _("Accepted")
        WAITING = "waiting", _("Waiting")
        REJECTED = "rejected", _("Rejected")

    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.PROTECT,
        related_name="submissions",
    )
    question = models.ForeignKey(
        Question,
        verbose_name=_("question"),
        on_delete=models.PROTECT,
        related_name="submissions",
    )
    lang = models.ForeignKey(
        Language,
        verbose_name=_("lang"),
        on_delete=models.PROTECT,
        related_name="submissions",
    )
    source_code = models.TextField(
        _("source code"),
    )
    solved = models.DateField(
        _("solved"),
    )
    snapshot = models.ImageField(
        _("snapshot"),
        upload_to=snapshot_upload_path,
    )
    course = models.ForeignKey(
        Course,
        verbose_name=_("course"),
        on_delete=models.PROTECT,
        related_name="submissions",
        null=True,
        blank=True,
    )
    runtime = models.CharField(
        _("runtime"),
        max_length=32,
        null=True,
        blank=True,
        help_text="262 ms",
    )
    memory = models.CharField(
        _("memory"),
        max_length=32,
        null=True,
        blank=True,
        help_text="19 MB",
    )
    runtime_rating = models.FloatField(
        _("runtime rating"),
        null=True,
        blank=True,
        help_text="69.65% --> 0.6965",
    )
    memory_rating = models.FloatField(
        _("memory rating"),
        null=True,
        blank=True,
        help_text="54.09% --> 0.5409",
    )
    difficulty = models.PositiveSmallIntegerField(
        _("difficulty"),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        help_text="1 is very easy, 5 is very hard.",
    )
    verify_status = models.CharField(
        _("verify status"),
        max_length=32,
        editable=False,
        choices=VerifyStatus.choices,
        default=VerifyStatus.WAITING,
    )
    verifier = models.ForeignKey(
        User,
        verbose_name=_("verifier"),
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
        editable=False,
    )
    verified = models.DateTimeField(
        _("verified"),
        null=True,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return f"{self.user} {self.question} {self.solved}"

    class Meta:
        verbose_name = _("submission")
        verbose_name_plural = _("submissions")


class VerifySubmission(Submission):
    class Meta:
        proxy = True
        verbose_name = _("verify submission")
        verbose_name_plural = _("verify submissions")
