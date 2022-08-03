from core.settings import env

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_JSONFIELD_ENABLED = True

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    # 'social_core.pipeline.user.user_details',
    # "app.auth_account.pipeline.save_profile",
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    "prompt": "select_account",
    "hd": "ntub.edu.tw",
}
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/admin'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/auth/social/complete/admin/"
SOCIAL_AUTH_SANITIZE_REDIRECTS = env("SOCIAL_AUTH_SANITIZE_REDIRECTS", default=False)
SOCIAL_AUTH_REDIRECT_IS_HTTPS = env("SOCIAL_AUTH_REDIRECT_IS_HTTPS", default=True)
