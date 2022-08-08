from django.core.management.base import BaseCommand

from app.problems.models import CodeSnippet, Language


class Command(BaseCommand):
    help = "Collecting languages from CodeSnippet."

    def handle(self, *args, **options):
        langs = set(
            CodeSnippet.objects.all().values_list(
                "lang_slug",
                "lang",
            ),
        )
        slugs = [it[0] for it in langs]
        exists_languages = Language.objects.filter(
            slug__in=slugs,
        ).values_list("slug", flat=True)
        languages = []
        for slug, name in langs:
            if slug in exists_languages:
                continue

            languages.append(
                Language(
                    slug=slug,
                    name=name,
                ),
            )

        languages = Language.objects.bulk_create(languages)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully collect {len(languages)} languages.",
            ),
        )
