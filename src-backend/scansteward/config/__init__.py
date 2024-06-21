from functools import lru_cache

from scansteward.config.settings import DjangoSettings
from scansteward.config.settings import PathSettings


@lru_cache(maxsize=1)
def get_django_settings() -> DjangoSettings:
    return DjangoSettings()


@lru_cache(maxsize=1)
def get_path_settings() -> PathSettings:
    return PathSettings()
