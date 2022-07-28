from typing import TypeVar

from django.db import models

__all__ = ["BaseManager"]


_T = TypeVar("_T", bound=models.Model, covariant=True)


class BaseManager(models.Manager[_T]):
    use_in_migrations = True
