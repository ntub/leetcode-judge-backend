from core.settings import env

SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "core.docs.info",
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "JWT": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Format: `Bearer <access_token>`",
        },
    },
}

DEFAULT_API_DOC_TYPE = env("DEFAULT_API_DOC_TYPE", default="swagger")

DEFAULT_API_VERSION = env("DEFAULT_API_VERSION", default="v1")
