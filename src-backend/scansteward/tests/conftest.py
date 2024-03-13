import random
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return 0


@pytest.fixture(scope="session", autouse=True)
def _seed_random():
    random.seed(0)


@pytest.fixture(scope="function")  # noqa: PT003
def temporary_directory() -> Generator[Path, None, None]:

    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir).resolve()
