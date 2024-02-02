from pathlib import Path
from typing import TYPE_CHECKING
from typing import Final

from blake3 import blake3
from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image

from images.models import Image as ImageModel


class Command(BaseCommand):
    help = "Indexes the given path(s) for new Images"

    IMAGE_EXTENSIONS: Final[set[str]] = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp"}

    def add_arguments(self, parser):
        parser.add_argument("paths", nargs="+", type=Path)

    def handle(self, *args, **options):
        for path in options["paths"]:
            if TYPE_CHECKING:
                assert isinstance(path, Path)
            for original_image in path.glob("**/*"):
                if original_image.suffix not in self.IMAGE_EXTENSIONS:
                    continue

                thumbnail_path: Path = (settings.THUMBNAIL_DIR / original_image.name).with_suffix(".webp")
                webp_path: Path = (settings.THUMBNAIL_DIR / original_image.name).with_suffix(".webp")
                original_path: Path = original_image.resolve()

                # Duplicate check
                image_hash = blake3(original_image.read_bytes(), max_threads=2).hexdigest()

                # Update path(s)
                existing_image = ImageModel.objects.filter(checksum=image_hash).first()
                if existing_image is not None:
                    changed = False
                    if existing_image.path != original_path:
                        existing_image.path = original_path
                        changed = True
                    if existing_image.thumbnail != thumbnail_path:
                        existing_image.thumbnail = thumbnail_path
                        changed = True
                    if existing_image.webp != webp_path:
                        existing_image.webp = webp_path
                        changed = True
                    if changed:
                        existing_image.save()
                    continue

                # New image then
                with Image.open(original_image) as im_file:
                    im_file.thumbnail((500, 500))
                    im_file.save(thumbnail_path)
                with Image.open(original_image) as im_file:
                    im_file.save(webp_path)

                ImageModel.objects.create(
                    file_size=original_image.stat().st_size,
                    checksum=image_hash,
                    original_path=str(original_image.resolve()),
                    thumbnail_path=str(thumbnail_path.resolve()),
                    webp_path=str(webp_path.resolve()),
                )
