import logging
import sys

import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from core.settings import env

logging.basicConfig(stream=sys.stderr)

SENTRY_DSN = env("SENTRY_DSN", default=None)
SENTRY_ENV = env("SENTRY_ENV", default=None)

if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENV,
        integrations=[
            DjangoIntegration(),
        ],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )
