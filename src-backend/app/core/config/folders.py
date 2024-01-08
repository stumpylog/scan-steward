from functools import lru_cache
from pathlib import Path

from pydantic import DirectoryPath

from app.core.config.base import AppBaseSettings


class DirectorySettings(AppBaseSettings):
    DATA_DIR: DirectoryPath = Path(__file__).parent.parent.parent / "data"


@lru_cache(maxsize=1)
def get_folder_settings() -> DirectorySettings:
    return DirectorySettings()
