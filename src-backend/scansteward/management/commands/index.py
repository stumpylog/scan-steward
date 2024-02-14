from pathlib import Path
from typing import TYPE_CHECKING
from typing import Final

from blake3 import blake3
from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image

from scansteward.models import Image as ImageModel


class Command(BaseCommand):
    help = "Indexes the given path(s) for new Images"

    IMAGE_EXTENSIONS: Final[set[str]] = {
        ".jpg",
        ".jpeg",
        ".png",
        ".tiff",
        ".tif",
        ".webp",
    }

    def add_arguments(self, parser):
        parser.add_argument("paths", nargs="+", type=Path)
        parser.add_argument("--source")
        parser.add_argument("--clear-source", action="store_true")
        parser.add_argument("--threads", default=2)

    def handle(self, *args, **options) -> None:  # noqa: ARG002
        self.source: str | None = options["source"]
        self.clear_source: bool = options["clear_source"]
        self.verbosity: int = options["verbosity"]
        self.threads: int = options["threads"]

        for path in options["paths"]:
            if TYPE_CHECKING:
                assert isinstance(path, Path)
            for original_image in path.glob("**/*"):
                self.stdout.write(self.style.SUCCESS(f"Indexing {original_image.name}"))
                if original_image.suffix not in self.IMAGE_EXTENSIONS:
                    if self.verbosity > 2:
                        self.stdout.write(self.style.NOTICE("Skipping due to extension"))
                    continue

                self.handle_single_image(original_image)

    def handle_single_image(self, image_path: Path) -> None:
        # Duplicate check
        image_hash = blake3(image_path.read_bytes(), max_threads=self.threads).hexdigest()

        # Update or create
        existing_image = ImageModel.objects.filter(checksum=image_hash).first()
        if existing_image is not None:
            self.handle_existing_image(existing_image, image_path)
        else:
            self.handle_new_image(image_path, image_hash)

    def handle_existing_image(self, existing_image: ImageModel, image_path: Path) -> None:
        self.stdout.write(self.style.NOTICE("  Image already indexed"))
        # Clear the source if requested
        if self.clear_source and existing_image.source is not None:
            self.stdout.write(self.style.NOTICE("  Clearing source"))
            existing_image.source = None
            existing_image.save()
        # Set the source if requested
        if (
            not self.clear_source
            and self.source is not None
            and (existing_image.source is None or existing_image.source != self.source)
        ):
            self.stdout.write(self.style.NOTICE(f"  Updating source to {self.source}"))
            existing_image.source = self.source
            existing_image.save()
        # Check for an updated location
        if image_path.resolve() != existing_image.original_path:
            existing_image.original_path = image_path.resolve()
            existing_image.save()
        self.stdout.write(self.style.SUCCESS(f"  {image_path.name} indexing completed"))

    def handle_new_image(self, image_path: Path, image_hash: str) -> None:
        thumbnail_path: Path = (settings.THUMBNAIL_DIR / image_path.name).with_suffix(".webp")
        webp_path: Path = (settings.FULL_SIZE_DIR / image_path.name).with_suffix(".webp")
        # New image then
        self.stdout.write(self.style.SUCCESS("  Creating thumbnail"))
        with Image.open(image_path) as im_file:
            im_file.thumbnail((500, 500))
            im_file.save(thumbnail_path)
        self.stdout.write(self.style.SUCCESS("  Creating WebP version"))
        with Image.open(image_path) as im_file:
            im_file.save(webp_path, quality=90)

        # Parse Faces
        self.stdout.write(self.style.SUCCESS("  Parsing faces"))

        # Parse Keywords
        self.stdout.write(self.style.SUCCESS("  Parsing keywords"))

        ImageModel.objects.create(
            file_size=image_path.stat().st_size,
            checksum=image_hash,
            original=str(image_path.resolve()),
            thumbnail=str(thumbnail_path.resolve()),
            full_size=str(webp_path.resolve()),
            source=self.source,
        )
        self.stdout.write(self.style.SUCCESS(f"  {image_path.name} indexing completed"))
