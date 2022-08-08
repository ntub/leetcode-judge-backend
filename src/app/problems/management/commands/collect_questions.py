from typing import List

from django.core.management.base import BaseCommand

from app.problems.models import Question
from app.problems.utils.leetcode import PageIndex, QuestionCollector


class Command(BaseCommand):
    help = "Collecting LeetCode all questions."

    def logger(self, index: PageIndex, questions: List[Question]) -> None:
        self.stdout.write(
            f"Page {index}, collected {len(questions)} questions.",
            ending="\r",
        )

    def handle(self, *args, **options):
        collector = QuestionCollector()
        collector.collect_question_list(self.logger)
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully collect questions.",
            ),
        )
