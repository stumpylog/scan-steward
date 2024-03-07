from datetime import datetime
from datetime import timezone


def now_string() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y:%m:%d %H:%M:%S.%f%z")
