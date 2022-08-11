from django.urls import include, path
from rest_framework.routers import SimpleRouter

from app.problems.api import views

app_name = "problems"

router = SimpleRouter(trailing_slash=False)
router.register("questions", views.QuestionViewSet, "questions")
router.register("languages", views.LanguageViewSet, "languages")

urlpatterns = [
    path("", include(router.urls)),
]
