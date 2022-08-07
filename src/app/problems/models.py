import uuid

from django.db import models

from utils.django.models import BaseModel


class Question(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
