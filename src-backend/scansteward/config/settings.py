from pathlib import Path

from pydantic import Field
from pydantic import SecretStr
from pydantic_extra_types.timezone_name import TimeZoneName
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from scansteward.config.types import DatabaseChoices


class AppBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="scan_steward_", secrets_dir="/run/secrets", str_strip_whitespace=True)


class DjangoSettings(AppBaseSettings):
    secret_key: SecretStr = Field(default="django-insecure-sy01il8rqt#832c6nx#2^a5@n_l(wy3v*dl&8-_*yu=1(=e%iv")
    debug: bool = True
    db_engine: DatabaseChoices = DatabaseChoices.Sqlite3
    timezone: TimeZoneName = Field(default="UTC")


class PathSettings(AppBaseSettings):
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
