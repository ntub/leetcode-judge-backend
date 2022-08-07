import random
import string

from django.apps import apps
from django.utils import timezone


def generate_serial_number(
    model_path: str,
    prefix: str,
    field_name="serial_number",
    characters=string.ascii_uppercase + string.digits,
    code_length=7,
    max_try=2000,
) -> str:
    model = apps.get_model(model_path)
    date = timezone.localdate().strftime("%Y%m%d")
    for _ in range(max_try):
        code = "".join(random.choices(characters, k=code_length))
        serial_number = f"{prefix}{date}{code}"

        if model.objects.filter(**{field_name: serial_number}).exists():
            continue

        return serial_number

    raise Exception("Can't found a serial_number")
