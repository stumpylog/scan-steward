from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin

from app.core.config import get_database_settings

session_config = AsyncSessionConfig(expire_on_commit=False)

config = SQLAlchemyAsyncConfig(
    connection_string=get_database_settings().DB_URL,
    session_config=session_config,
)

sql_alchemy_plugin = SQLAlchemyPlugin(config=config)
