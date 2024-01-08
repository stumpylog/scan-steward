from functools import cached_property
from functools import lru_cache
from typing import Literal

from pydantic import PostgresDsn

from app.core.config.base import AppBaseSettings
from app.core.config.folders import get_folder_settings


class DatabaseTypeSettings(AppBaseSettings):
    DB_TYPE: Literal["sqlite", "postgres"] = "sqlite"


class SqliteDatabaseSettings(AppBaseSettings):
    @cached_property
    def DB_URL(self) -> str:  # noqa: N802
        dir_settings = get_folder_settings()
        return f"sqlite+aiosqlite:///{dir_settings.DATA_DIR}/scansteward.sqlite3"


class PostgresDatabaseSettings(AppBaseSettings):
    DB_URL: PostgresDsn


@lru_cache(maxsize=1)
def get_database_settings() -> SqliteDatabaseSettings | PostgresDatabaseSettings:
    type_setting = DatabaseTypeSettings()
    if type_setting.DB_TYPE == "sqlite":
        return SqliteDatabaseSettings()
    elif type_setting.DB_TYPE == "postgres":  # pragma: no cover
        return PostgresDatabaseSettings()

    raise NotImplementedError(type_setting.DB_TYPE)  # pragma: no cover
