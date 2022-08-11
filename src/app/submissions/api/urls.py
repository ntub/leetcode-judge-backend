from django.urls import include, path
from rest_framework.routers import SimpleRouter

from app.submissions.api import views

app_name = "submissions"

router = SimpleRouter(trailing_slash=False)
router.register("submissions", views.SubmissionViewSet, "submissions")

urlpatterns = [
    path("", include(router.urls)),
]
