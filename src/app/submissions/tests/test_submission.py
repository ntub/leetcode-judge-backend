from typing import List, NamedTuple

from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from rest_framework import test

from app.courses.models import Course
from app.problems.models import CodeSnippet, Language, Question
from app.submissions.api.serializers import SubmissionSerializer
from app.submissions.tests.prepare import CourseFactory, UserFactory
from app.users.models import User

_Request = NamedTuple(
    "_Request",
    [("user", User)],
)


class SubmissionTest(test.APITestCase):
    fixtures = ["problems"]
    student: User
    course: Course
    questions: List[Question]
    languages: List[Language]

    @classmethod
    def setUpTestData(cls) -> None:
        for _ in range(10):
            UserFactory()

        cls.student = UserFactory()
        cls.questions = list(
            Question.objects.filter(difficulty="Easy").order_by("question_id")[:3],
        )
        cls.languages = list(
            Language.objects.filter(
                slug__in=list(
                    CodeSnippet.objects.filter(question__in=cls.questions).values_list(
                        "lang_slug",
                        flat=True,
                    )[:5],
                ),
            ),
        )
        cls.course = CourseFactory(
            questions=cls.questions,
            users=User.objects.all(),
            languages=cls.languages,
        )

    def test_serializer(self) -> None:
        faker = Faker()
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=faker.image(),
            content_type="image/jpeg",
        )
        data = {
            "question_title_slug": self.questions[0].title_slug,
            "lang_slug": self.languages[0].slug,
            "course_code": self.course.code,
            "source_code": faker.text(),
            "solved": faker.date_time().strftime("%Y-%m-%d"),
            "snapshot": image,
        }
        request = _Request(user=self.student)
        serializer = SubmissionSerializer(
            data=data,
            context={
                "request": request,
            },
        )
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_lang_not_in_course(self) -> None:
        faker = Faker()
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=faker.image(),
            content_type="image/jpeg",
        )
        data = {
            "question_title_slug": self.questions[0].title_slug,
            "lang_slug": (
                Language.objects.exclude(  # type: ignore
                    slug__in=list(
                        map(lambda o: o.slug, self.languages),
                    ),
                )
                .first()
                .slug
            ),
            "course_code": self.course.code,
            "source_code": faker.text(),
            "solved": faker.date_time().strftime("%Y-%m-%d"),
            "snapshot": image,
        }
        request = _Request(user=self.student)
        serializer = SubmissionSerializer(
            data=data,
            context={
                "request": request,
            },
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("course", serializer.errors)

    def test_user_not_in_course(self) -> None:
        faker = Faker()
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=faker.image(),
            content_type="image/jpeg",
        )
        data = {
            "question_title_slug": self.questions[0].title_slug,
            "lang_slug": self.languages[0].slug,
            "course_code": self.course.code,
            "source_code": faker.text(),
            "solved": faker.date_time().strftime("%Y-%m-%d"),
            "snapshot": image,
        }
        request = _Request(user=UserFactory())
        serializer = SubmissionSerializer(
            data=data,
            context={
                "request": request,
            },
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("course", serializer.errors)

    def test_question_not_in_course(self) -> None:
        faker = Faker()
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=faker.image(),
            content_type="image/jpeg",
        )
        data = {
            "question_title_slug": (
                Question.objects.filter(difficulty="Hard")  # type: ignore
                .first()
                .title_slug
            ),
            "lang_slug": self.languages[0].slug,
            "course_code": self.course.code,
            "source_code": faker.text(),
            "solved": faker.date_time().strftime("%Y-%m-%d"),
            "snapshot": image,
        }
        request = _Request(user=self.student)
        serializer = SubmissionSerializer(
            data=data,
            context={
                "request": request,
            },
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("course", serializer.errors)

    def test_lang_not_in_question(self) -> None:
        faker = Faker()
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=faker.image(),
            content_type="image/jpeg",
        )
        data = {
            "question_title_slug": self.questions[0].title_slug,
            "lang_slug": Language.objects.create(name="Test", slug="test").slug,
            "course_code": self.course.code,
            "source_code": faker.text(),
            "solved": faker.date_time().strftime("%Y-%m-%d"),
            "snapshot": image,
        }
        request = _Request(user=self.student)
        serializer = SubmissionSerializer(
            data=data,
            context={
                "request": request,
            },
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("question", serializer.errors)
