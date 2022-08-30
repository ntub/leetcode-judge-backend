import random
import string

from django.apps import apps
from django.utils import timezone


def generate_serial_number(
    model_path: str,
    prefix: str,
    field_name: str = "serial_number",
    characters: str = string.ascii_uppercase + string.digits,
    code_length: int = 3,
    max_try: int = 2000,
) -> str:
    model = apps.get_model(model_path)
    date = timezone.localdate().strftime("%Y%m%d")[-6:]
    for _ in range(max_try):
        code = "".join(random.choices(characters, k=code_length))
        serial_number = f"{prefix}{date}{code}"

        if model.objects.filter(**{field_name: serial_number}).exists():
            continue

        return serial_number

    raise Exception("Can't found a serial_number")
