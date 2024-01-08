from collections.abc import AsyncIterator

import pytest
from httpx import AsyncClient
from litestar import Litestar
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool

# https://gist.github.com/qodot/c2eaee272a6923d86305c16ffd80b3cf


@pytest.fixture(name="app")
def fx_app() -> Litestar:
    """
    App fixture.

    Returns:
        An application instance, configured via plugin.
    """
    from app.main import app

    return app


@pytest.fixture(name="engine")
async def fx_engine() -> AsyncEngine:
    """
    SQLite instance for end-to-end testing, created in memort

    Returns:
        Async SQLAlchemy engine instance.
    """
    return create_async_engine(
        url="sqlite+aiosqlite:///:memory:",
        echo=False,
        poolclass=StaticPool,
    )


@pytest.fixture(name="sessionmaker")
def fx_session_maker_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """
    Creates an async sessionmaker, bound to the *test* database
    """
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
def _patch_database_config(
    app: "Litestar",
    engine: AsyncEngine,
    sessionmaker: async_sessionmaker[AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Monkey patches the configuration of the application to use *our* async session manager
    """
    from app.core.plugins.database import config

    monkeypatch.setitem(app.state, config.engine_app_state_key, engine)
    monkeypatch.setitem(
        app.state,
        config.session_maker_app_state_key,
        sessionmaker,
    )


@pytest.fixture(autouse=True)
async def _init_database(engine: AsyncEngine):
    """
    initialize the test database, with all tables creates

    """

    from app.core.models.base import AppBaseModel

    metadata = AppBaseModel.metadata
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)


@pytest.fixture(name="test_client")
async def fx_client(app: Litestar) -> AsyncIterator[AsyncClient]:
    """
    Async client that calls requests on the app.

    ValueError: The future belongs to a different loop than the one specified as the loop argument
    """
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client
