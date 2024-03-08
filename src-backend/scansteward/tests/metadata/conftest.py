from pathlib import Path

import pytest


@pytest.fixture()
def sample_one_jpeg(image_sample_dir: Path) -> Path:
    return image_sample_dir / "sample1.jpg"


@pytest.fixture()
def sample_two_jpeg(image_sample_dir: Path) -> Path:
    return image_sample_dir / "sample2.jpg"


@pytest.fixture()
def sample_three_jpeg(image_sample_dir: Path) -> Path:
    return image_sample_dir / "sample3.jpg"


@pytest.fixture()
def sample_four_jpeg(image_sample_dir: Path) -> Path:
    return image_sample_dir / "sample4.jpg"
