from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from app.users.models import User
from utils.django.admin import AuditModelAdmin


@admin.register(User)
class UserAdmin(AuditModelAdmin[User], DjangoUserAdmin):
    list_display = ("username", "is_staff", "created")
    ordering = ("created", "pk")
    filter_horizontal = ("groups", "user_permissions")
    date_hierarchy = "created"
    readonly_fields = ("created", "modified", "date_joined")
