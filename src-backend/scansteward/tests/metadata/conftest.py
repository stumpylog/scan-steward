import shutil
from pathlib import Path

import pytest

from scansteward.imageops.models import ImageMetadata


@pytest.fixture(scope="session")
def sample_one_metadata_original(fixture_directory: Path) -> ImageMetadata:
    return ImageMetadata.model_validate_json((fixture_directory / "sample1.jpg.json").read_text())


@pytest.fixture(scope="session")
def sample_two_metadata_original(fixture_directory: Path) -> ImageMetadata:
    return ImageMetadata.model_validate_json((fixture_directory / "sample2.jpg.json").read_text())


@pytest.fixture(scope="session")
def sample_three_metadata_original(fixture_directory: Path) -> ImageMetadata:
    return ImageMetadata.model_validate_json((fixture_directory / "sample3.jpg.json").read_text())


@pytest.fixture(scope="session")
def sample_four_metadata_original(fixture_directory: Path) -> ImageMetadata:
    return ImageMetadata.model_validate_json((fixture_directory / "sample4.jpg.json").read_text())


@pytest.fixture()
def sample_one_metadata_copy(
    tmp_path: Path,
    sample_one_original_file: Path,
    sample_one_metadata_original: ImageMetadata,
) -> ImageMetadata:
    cpy = sample_one_metadata_original.model_copy(deep=True)
    cpy.SourceFile = shutil.copy(sample_one_original_file, tmp_path / sample_one_original_file.name)
    return cpy


@pytest.fixture()
def sample_two_metadata_copy(
    tmp_path: Path,
    sample_two_original_file: Path,
    sample_two_metadata_original: ImageMetadata,
) -> ImageMetadata:
    cpy = sample_two_metadata_original.model_copy(deep=True)
    cpy.SourceFile = shutil.copy(sample_two_original_file, tmp_path / sample_two_original_file.name)
    return cpy


@pytest.fixture()
def sample_three_metadata_copy(
    tmp_path: Path,
    sample_three_original_file: Path,
    sample_three_metadata_original: ImageMetadata,
) -> ImageMetadata:
    cpy = sample_three_metadata_original.model_copy(deep=True)
    cpy.SourceFile = shutil.copy(sample_three_original_file, tmp_path / sample_three_original_file.name)
    return cpy


@pytest.fixture()
def sample_four_metadata_copy(
    tmp_path: Path,
    sample_four_original_file: Path,
    sample_four_metadata_original: ImageMetadata,
) -> ImageMetadata:
    cpy = sample_four_metadata_original.model_copy(deep=True)
    cpy.SourceFile = shutil.copy(sample_four_original_file, tmp_path / sample_four_original_file.name)
    return cpy
