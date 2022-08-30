from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin

from app.bulletins.models import Announcement, AttachFile
from utils.django.admin import AuditModelAdmin


class AttachFileInline(admin.TabularInline["AttachFile", "Announcement"]):
    model = AttachFile
    max_num = 10


@admin.register(Announcement)
class AnnouncementAdmin(AuditModelAdmin[Announcement]):
    list_display = ("title", "status", "created")
    list_filter = ("status", "created", "activate_date", "deactivate_date", "courses")
    search_fields = ("title",)
    ordering = ("-modified", "-created")
    date_hierarchy = "created"
    readonly_fields = ("created", "modified")
    filter_horizontal = ("courses",)
    inlines = [
        AttachFileInline,
    ]
    formfield_overrides = {
        RichTextUploadingField: {"widget": CKEditorUploadingWidget},
    }
