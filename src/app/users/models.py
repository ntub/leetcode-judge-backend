from datetime import datetime
from typing import Any, Optional

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractUser,
    PermissionsMixin,
    UserManager as DjangoUserManager,
)
from django.utils.translation import gettext_lazy as _

from utils.django.managers import BaseManager
from utils.django.models import BaseModel


class UserManager(BaseManager["User"], DjangoUserManager["User"]):
    use_in_migrations = True

    def _create_user(
        self,
        username: str,
        password: Optional[str],
        **extra_fields: Any,
    ) -> "User":
        if not username:
            raise ValueError("The given username must be set")

        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(  # type: ignore[override]
        self,
        username: str,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> "User":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(  # type: ignore[override]
        self,
        username: str,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class User(BaseModel, AbstractUser, PermissionsMixin):
    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return str(self.username)

    @property
    def date_joined(self) -> datetime:
        return self.created
