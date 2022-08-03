from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from core.docs import DEFAULT_API_DOC_URL, SchemaView

v1_urlpatterns = [
    path("auth/", include("app.users.api.urls")),
]

api_urlpatterns = [
    # Resource urls
    path("v1/", include((v1_urlpatterns, "v1"))),
    # Docs urls
    path("swagger/", SchemaView.with_ui(), name="swagger"),
    path("redoc/", SchemaView.with_ui(renderer="redoc"), name="redoc"),
    path("docs/", RedirectView.as_view(pattern_name=DEFAULT_API_DOC_URL), name="docs"),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((api_urlpatterns, "api"))),
]
