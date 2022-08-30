from typing import Any

import factory

from app.courses.models import Course
from app.users.models import User


class UserFactory(factory.django.DjangoModelFactory):  # type: ignore
    class Meta:
        model = User

    username = factory.Faker("user_name", locale="zh_TW")
    first_name = factory.Faker("first_name", locale="zh_TW")
    last_name = factory.Faker("last_name", locale="zh_TW")
    email = factory.Faker("email", locale="zh_TW")


class CourseFactory(factory.django.DjangoModelFactory):  # type: ignore
    class Meta:
        model = Course

    title = factory.Faker("sentence", locale="zh_TW")
    description = factory.Faker("text", locale="zh_TW")

    @factory.post_generation  # type: ignore
    def questions(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        if not create:
            return

        if extracted:
            self.questions.add(*extracted)

    @factory.post_generation  # type: ignore
    def users(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        if not create:
            return

        if extracted:
            self.users.add(*extracted)

    @factory.post_generation  # type: ignore
    def languages(self, create: Any, extracted: Any, **kwargs: Any) -> None:
        if not create:
            return

        if extracted:
            self.languages.add(*extracted)
