import pathlib

import django_stubs_ext
import environ

from split_settings.tools import include, optional

env = environ.Env()
env_file = pathlib.Path(__file__).parent / ".env"

if env_file.exists():
    env.read_env()

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
django_stubs_ext.monkeypatch()


include(
    "common.py",
    "components/*.py",
    optional("local_settings.py"),
)
