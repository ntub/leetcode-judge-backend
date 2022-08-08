from django.contrib import admin

from app.problems.models import CodeSnippet, Language, Question, TopicTag


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin[Question]):
    list_display = ("title_slug", "title", "difficulty")
    search_fields = ("title_slug", "title")
    list_filter = ("difficulty",)
    ordering = ("question_id", "question_frontend_id")


@admin.register(TopicTag)
class TopicTagAdmin(admin.ModelAdmin[TopicTag]):
    list_display = ("slug", "name")
    search_fields = ("slug", "name")


@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin[CodeSnippet]):
    list_display = ("lang_slug", "lang", "question")
    search_fields = (
        "lang_slug",
        "lang",
        "question__title",
        "question__title_slug",
        "question__difficulty",
    )
    list_select_related = ("question",)
    list_filter = ("lang_slug", "question__difficulty")


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin[Language]):
    list_display = ("slug", "name")
    search_fields = ("slug", "name")
