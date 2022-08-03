from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser

DEFAULT_API_DOC_TYPE = getattr(settings, "DEFAULT_API_DOC_TYPE", "swagger")
DEFAULT_API_DOC_URL = f"api:{DEFAULT_API_DOC_TYPE}"

DEFAULT_API_VERSION = getattr(settings, "DEFAULT_API_VERSION", "v1")

SchemaView = get_schema_view(
    openapi.Info(title="API Documents", default_version=DEFAULT_API_VERSION),
    public=True,
    authentication_classes=(SessionAuthentication,),
    permission_classes=(IsAdminUser,),
)
