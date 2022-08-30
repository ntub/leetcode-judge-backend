import json

from typing import Any, Dict

import humps

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import ActivatorModel, ActivatorModelManager

from utils.django.managers import BaseManager
from utils.django.models import UUIDModel


class TopicTag(UUIDModel):
    name = models.CharField(
        _("name"),
        max_length=255,
    )
    slug = models.CharField(
        _("slug"),
        max_length=255,
        unique=True,
    )

    def __str__(self) -> str:
        return f"{self.name}({self.slug})"

    class Meta:
        verbose_name = _("topic tag")
        verbose_name_plural = _("topic tags")


class QuestionManager(BaseManager["Question"]):
    pass


class Question(UUIDModel):
    question_id = models.CharField(
        _("question id"),
        max_length=16,
    )
    question_frontend_id = models.CharField(
        _("question frontend id"),
        max_length=16,
    )
    title = models.CharField(
        _("title"),
        max_length=255,
    )
    title_slug = models.CharField(
        _("title slug"),
        max_length=255,
        unique=True,
    )
    content = models.TextField(
        _("content"),
        null=True,
        blank=True,
    )
    difficulty = models.CharField(
        _("difficulty"),
        max_length=64,
    )
    likes = models.PositiveIntegerField(
        _("likes"),
        default=0,
        blank=True,
    )
    dislikes = models.PositiveIntegerField(
        _("dislikes"),
        default=0,
        blank=True,
    )
    similar_questions = models.JSONField(
        _("similar questions"),
        default=list,
    )
    category_title = models.CharField(
        _("category title"),
        max_length=255,
    )
    topic_tags = models.ManyToManyField(
        TopicTag,
        related_name="questions",
        verbose_name=_("topic tags"),
        blank=True,
    )
    stats = models.JSONField(_("stats"))
    hints = models.JSONField(
        _("hints"),
        default=list,
    )
    meta_data = models.JSONField(_("meta data"))
    judge_type = models.CharField(
        _("judge type"),
        max_length=32,
    )
    env_info = models.JSONField(_("env info"))
    sample_test_case = models.TextField(
        _("sample test case"),
        blank=True,
        null=True,
    )
    example_testcases = models.TextField(
        _("example testcases"),
        blank=True,
        null=True,
    )
    objects = QuestionManager()

    @classmethod
    def from_leetcode(cls, data: Dict[str, Any]) -> "Question":
        data["similar_questions"] = humps.decamelize(  # type: ignore
            json.loads(
                data.get("similar_questions", "{}"),
            ),
        )
        data["stats"] = humps.decamelize(  # type: ignore
            json.loads(
                data.get("stats", "{}"),
            ),
        )
        data["hints"] = humps.decamelize(  # type: ignore
            data.get("hints", []),
        )
        data["meta_data"] = humps.decamelize(  # type: ignore
            json.loads(
                data.get("meta_data", "{}"),
            ),
        )
        data["env_info"] = humps.decamelize(  # type: ignore
            json.loads(
                data.get("env_info", "{}"),
            ),
        )
        fields = [field.name for field in cls._meta.fields]
        data = {k: v for k, v in data.items() if k in fields}
        return cls(**data)

    def __str__(self) -> str:
        return f"[{self.difficulty}]{self.title}({self.title_slug})"

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")


class CodeSnippet(UUIDModel):
    lang = models.CharField(
        _("lang"),
        max_length=32,
    )
    lang_slug = models.CharField(
        _("lang slug"),
        max_length=32,
    )
    code = models.TextField(
        _("code"),
    )
    question = models.ForeignKey(
        Question,
        verbose_name=_("question"),
        related_name="code_snippets",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.question} - {self.lang}"

    class Meta:
        verbose_name = _("code snippet")
        verbose_name_plural = _("code snippets")


class LanguageManager(
    ActivatorModelManager,  # type: ignore
    BaseManager["Language"],
):
    pass


class Language(ActivatorModel, UUIDModel):  # type: ignore
    name = models.CharField(
        _("lang"),
        max_length=32,
    )
    slug = models.CharField(
        _("lang slug"),
        max_length=32,
        unique=True,
    )
    objects = LanguageManager()

    def __str__(self) -> str:
        return f"{self.name} - {self.slug}"

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")
