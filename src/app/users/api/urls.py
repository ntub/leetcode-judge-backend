from django.urls import include, path
from rest_framework.routers import SimpleRouter

from app.users.api import views

app_name = "users"

router = SimpleRouter(trailing_slash=False)
router.register("token", views.AuthViewSet, "auth")

urlpatterns = [
    path("", include(router.urls)),
]
