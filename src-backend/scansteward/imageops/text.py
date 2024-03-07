from __future__ import annotations

from typing import TYPE_CHECKING

from scansteward.imageops.metadata import bulk_read_image_metadata
from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.metadata import read_image_metadata
from scansteward.imageops.metadata import write_image_metadata

if TYPE_CHECKING:
    from pathlib import Path

    from scansteward.imageops.models import ImageMetadata


def read_title(image_path: Path) -> ImageMetadata:
    return read_image_metadata(image_path, read_title=True)


def bulk_read_title(images: list[Path]) -> list[ImageMetadata]:
    return bulk_read_image_metadata(images, read_title=True)


def write_title(metadata: ImageMetadata) -> None:
    return write_image_metadata(metadata)


def bulk_write_title(metadata: list[ImageMetadata]) -> None:
    return bulk_write_image_metadata(metadata)


def read_description(image_path: Path) -> ImageMetadata:
    return read_image_metadata(image_path, read_description=True)


def bulk_read_description(images: list[Path]) -> list[ImageMetadata]:
    return bulk_read_image_metadata(images, read_description=True)


def write_description(metadata: ImageMetadata) -> None:
    return write_image_metadata(metadata)


def bulk_write_description(metadata: list[ImageMetadata]) -> None:
    return bulk_write_image_metadata(metadata)
