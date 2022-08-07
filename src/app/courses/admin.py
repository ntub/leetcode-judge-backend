from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from app.courses.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin["Course"]):
    list_display = ("title", "created")
    ordering = ("created", "pk")
    date_hierarchy = "created"
    readonly_fields = ("created", "modified")
