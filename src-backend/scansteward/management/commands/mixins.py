from pathlib import Path
from typing import Final

from blake3 import blake3
from imagehash import average_hash
from PIL import Image

from scansteward.models import Image as ImageModel


class KeywordNameMixin:
    DATE_KEYWORD: Final[str] = "Dates"
    PEOPLE_KEYWORD: Final[str] = "People"
    LOCATION_KEYWORD: Final[str] = "Locations"


class ImageHasherMixin:
    def hash_file(self, filepath: Path, *, hash_threads: int = 4) -> str:
        return blake3(
            filepath.read_bytes(),
            max_threads=hash_threads,
        ).hexdigest()

    def update_image_hash(self, image: ImageModel, *, hash_threads: int = 4) -> None:
        with Image.open(image.original_path) as im_file:
            image.phash = str(average_hash(im_file))

        image.original_checksum = self.hash_file(image.original_path, hash_threads=hash_threads)
        image.full_size_checksum = self.hash_file(image.full_size_path, hash_threads=hash_threads)
        image.thumbnail_checksum = self.hash_file(image.thumbnail_path, hash_threads=hash_threads)

        image.save()
