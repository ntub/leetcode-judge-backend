from django.urls import include, path
from rest_framework.routers import SimpleRouter

from app.bulletins.api import views

app_name = "bulletins"

router = SimpleRouter(trailing_slash=False)
router.register("announcements", views.AnnouncementViewSet, "announcements")

urlpatterns = [
    path("", include(router.urls)),
]
