from django.urls import include, path
from rest_framework.routers import SimpleRouter

from app.courses.api import views

app_name = "courses"

router = SimpleRouter(trailing_slash=False)
router.register("courses", views.CourseViewSet, "courses")

urlpatterns = [
    path("", include(router.urls)),
]
