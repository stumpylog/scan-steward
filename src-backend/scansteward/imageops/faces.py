from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from scansteward.imageops.metadata import bulk_read_image_metadata
from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.metadata import read_image_metadata
from scansteward.imageops.metadata import write_image_metadata

if TYPE_CHECKING:
    from pathlib import Path

    from scansteward.imageops.models import ImageMetadata

logger = logging.getLogger(__name__)


def read_faces(image_path: Path) -> ImageMetadata:
    return read_image_metadata(image_path, read_regions=True)


def bulk_read_faces(images: list[Path]) -> list[ImageMetadata]:
    return bulk_read_image_metadata(images, read_regions=True)


def write_faces(metadata: ImageMetadata) -> None:
    return write_image_metadata(metadata)


def bulk_write_faces(metadata: list[ImageMetadata]) -> None:
    return bulk_write_image_metadata(metadata)
