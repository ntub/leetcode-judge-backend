from typing import Any, Callable, Dict, List, NewType, Optional

from app.problems.models import CodeSnippet, Question, TopicTag
from app.problems.utils.leetcode.api import LeetCodeGraphAPI

PageIndex = NewType("PageIndex", int)


class QuestionCollector:
    def __init__(self) -> None:
        self.api = LeetCodeGraphAPI()

    def collect_question_list(
        self,
        log_fn: Optional[Callable[[PageIndex, List[Question]], None]] = None,
    ) -> None:
        index = 0
        for question_list in self.api.question_list_iterator():
            title_slugs = [item["title_slug"] for item in question_list]
            questions = self.collect_questions(title_slugs)

            index += 1
            if log_fn:
                log_fn(PageIndex(index), questions)

    def collect_questions(self, title_slugs: List[str]) -> List[Question]:
        questions: List[Question] = []
        question_code_snippet_mapping: Dict[str, List[CodeSnippet]] = {}
        question_topic_tag_mapping: Dict[str, List[TopicTag]] = {}

        exists_title_slugs = Question.objects.filter(
            title_slug__in=title_slugs,
        ).values_list(
            "title_slug",
            flat=True,
        )

        for title_slug in title_slugs:
            if title_slug in exists_title_slugs:
                continue

            question_data = self.api.question(title_slug)
            topic_tag_data = question_data.get("topic_tags", [])
            code_snippet_data = question_data.get("code_snippets", [])
            obj = Question.from_leetcode(question_data)
            topic_tags = self.collect_topic_tags(
                topic_tag_data or [],
            )
            question_topic_tag_mapping[obj.title_slug] = topic_tags
            question_code_snippet_mapping[obj.title_slug] = self.collect_code_snippet(
                obj,
                code_snippet_data or [],
            )
            questions.append(obj)

        questions = Question.objects.bulk_create(questions)
        for question in questions:
            code_snippets = question_code_snippet_mapping[question.title_slug]
            topic_tags = question_topic_tag_mapping[question.title_slug]
            if topic_tags:
                from pprint import pprint

                pprint(topic_tags)
                question.topic_tags.add(*topic_tags)

            if code_snippets:
                CodeSnippet.objects.bulk_create(code_snippets)

        return questions

    def collect_topic_tags(self, data: List[Dict[str, Any]]) -> List[TopicTag]:
        topic_tag_slugs = [it["slug"] for it in data]
        exists_objs_mapping = {
            obj.slug: obj for obj in TopicTag.objects.filter(slug__in=topic_tag_slugs)
        }
        new_objs: List[TopicTag] = []
        exists_objs: List[TopicTag] = []

        for item in data:
            if (slug := item["slug"]) in exists_objs_mapping:
                exists_objs.append(exists_objs_mapping[slug])
            else:
                new_objs.append(TopicTag(**item))

        new_objs = TopicTag.objects.bulk_create(new_objs)
        return new_objs + exists_objs

    def collect_code_snippet(
        self,
        question: Question,
        data: List[Dict[str, Any]],
    ) -> List[CodeSnippet]:
        code_snippets: List[CodeSnippet] = []

        for item in data:
            code_snippets.append(
                CodeSnippet(
                    question=question,
                    **item,
                ),
            )

        return code_snippets
