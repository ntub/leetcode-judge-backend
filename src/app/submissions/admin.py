from django.contrib import admin
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_object_actions import DjangoObjectActions

from app.submissions.models import Submission, VerifySubmission
from utils.django.admin import AuditModelAdmin, action_display


@admin.register(Submission)
class SubmissionAdmin(AuditModelAdmin[Submission]):
    list_display = ("user", "question", "solved", "verify_status")
    search_fields = ("user__username", "question__title")
    list_filter = ("verify_status", "difficulty", "verified", "solved")
    ordering = ("-solved", "-verified")
    list_select_related = ("user", "question", "lang")
    autocomplete_fields = ("user", "question", "lang", "course")


@admin.register(VerifySubmission)
class VerifySubmissionAdmin(DjangoObjectActions, SubmissionAdmin):  # type: ignore
    change_actions = ("accept", "reject")
    readonly_fields = (
        "user",
        "question",
        "lang",
        "source_code",
        "solved",
        "difficulty",
        "snapshot",
        "verify_status",
        "verifier",
        "verified",
        "created",
        "modified",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "question",
                    "lang",
                    "source_code",
                    "solved",
                    "difficulty",
                ),
            },
        ),
        (
            _("Submission result"),
            {
                "fields": (
                    "snapshot",
                    "runtime",
                    "memory",
                    "runtime_rating",
                    "memory_rating",
                ),
            },
        ),
        (
            _("Verify info"),
            {
                "fields": (
                    "verify_status",
                    "verifier",
                    "verified",
                    "created",
                    "modified",
                ),
            },
        ),
    )

    @action_display(  # type: ignore
        label=_("Accept"),
        attrs={
            "style": "background: green",
        },
    )
    def accept(self, request: HttpRequest, obj: VerifySubmission) -> None:
        obj.verify_status = VerifySubmission.VerifyStatus.ACCEPTED
        obj.verifier = request.user  # type: ignore
        obj.verified = timezone.localtime()
        obj.save()

    @action_display(  # type: ignore
        label=_("Reject"),
        attrs={
            "style": "background: red",
        },
    )
    def reject(self, request: HttpRequest, obj: VerifySubmission) -> None:
        obj.verify_status = VerifySubmission.VerifyStatus.REJECTED
        obj.verifier = request.user  # type: ignore
        obj.verified = timezone.localtime()
        obj.save()

    class Media:
        css = {
            "all": (
                "highlight/styles/default.min.css",
                "submissions/verification.css",
            ),
        }
        js = (
            "highlight/highlight.min.js",
            "submissions/verification.js",
        )
