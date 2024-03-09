from collections.abc import Generator
from pathlib import Path

import pytest
from faker import Faker


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return 12345


@pytest.fixture()
def create_image_object(faker: Faker):
    import random

    from scansteward.models import Image

    return Image.objects.create(
        file_size=random.randint(1, 1_000_000),  # noqa: S311
        checksum=faker.sha1()[:64],
        original=faker.file_path(category="image"),
    )


@pytest.fixture(scope="function")  # noqa: PT003
def temporary_directory() -> Generator[Path, None, None]:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir).resolve()


@pytest.fixture(scope="session")
def sample_dir() -> Path:
    return Path(__file__).parent / "samples"


@pytest.fixture(scope="session")
def image_sample_dir(sample_dir: Path) -> Path:
    return sample_dir / "images"
