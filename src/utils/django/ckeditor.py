import random
import string

from django.http.request import HttpRequest


def get_filename(filename: str, request: HttpRequest) -> str:
    rand_str = "".join(
        random.choices(
            (string.ascii_lowercase + string.digits),
            k=12,
        ),
    )
    text = filename.lower().replace("-", "")
    return f"{rand_str}_{text}"
