from django.contrib import admin

from app.courses.models import Course
from utils.django.admin import AuditModelAdmin


@admin.register(Course)
class CourseAdmin(AuditModelAdmin[Course]):
    list_display = ("code", "title", "created")
    search_fields = ("code", "title")
    ordering = ("-created", "-modified", "code")
    date_hierarchy = "created"
    readonly_fields = ("created", "modified")
    filter_horizontal = ("questions", "users", "languages")
