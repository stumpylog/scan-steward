from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class AppBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SCAN_STEWARD_")
