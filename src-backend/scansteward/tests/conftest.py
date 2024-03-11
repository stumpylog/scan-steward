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


@pytest.fixture(scope="function")  # noqa: PT003
def django_base_dir(settings) -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture(scope="session")
def sample_dir() -> Path:
    return Path(__file__).parent / "samples"


@pytest.fixture(scope="session")
def image_sample_dir(sample_dir: Path) -> Path:
    return sample_dir / "images"


@pytest.fixture(scope="session")
def sample_one_jpeg(image_sample_dir: Path) -> Path:
    return image_sample_dir / "sample1.jpg"


@pytest.fixture(scope="session")
def sample_two_jpeg(image_sample_dir: Path) -> Path:
    return image_sample_dir / "sample2.jpg"


@pytest.fixture(scope="session")
def sample_three_jpeg(image_sample_dir: Path) -> Path:
    return image_sample_dir / "sample3.jpg"


@pytest.fixture(scope="session")
def sample_four_jpeg(image_sample_dir: Path) -> Path:
    return image_sample_dir / "sample4.jpg"


@pytest.fixture(scope="session")
def all_sample_jpegs(
    sample_one_jpeg: Path,
    sample_two_jpeg: Path,
    sample_three_jpeg: Path,
    sample_four_jpeg: Path,
) -> list[Path]:
    return [sample_one_jpeg, sample_two_jpeg, sample_three_jpeg, sample_four_jpeg]
