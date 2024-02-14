from enum import IntEnum
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Final

from blake3 import blake3
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image

from scansteward.models import Image as ImageModel


class Verbosity(IntEnum):
    MINIMAL = 0
    NORMAL = 1
    VERBOSE = 2
    DEBUG = 3


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
        self.verbosity: Verbosity = Verbosity(options["verbosity"])
        self.threads: int = options["threads"]

        for path in options["paths"]:
            if TYPE_CHECKING:
                assert isinstance(path, Path)
            for directory_item in path.glob("**/*"):
                if directory_item.is_dir():
                    continue
                if directory_item.suffix not in self.IMAGE_EXTENSIONS:
                    if self.verbosity >= Verbosity.VERBOSE:
                        self.stdout.write(self.style.NOTICE("Skipping due to extension"))
                    continue

                self.stdout.write(self.style.SUCCESS(f"Indexing {directory_item.name}"))
                self.handle_single_image(directory_item)

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
        with transaction.atomic():

            new_img = ImageModel.objects.create(
                file_size=image_path.stat().st_size,
                checksum=image_hash,
                original=str(image_path.resolve()),
                source=self.source,
            )

            self.stdout.write(self.style.SUCCESS("  Creating thumbnail"))
            with Image.open(image_path) as im_file:
                im_file.thumbnail((500, 500))
                im_file.save(new_img.thumbnail_path)
            self.stdout.write(self.style.SUCCESS("  Creating WebP version"))
            with Image.open(image_path) as im_file:
                im_file.save(new_img.full_size_path, quality=90)

            # Parse Faces
            self.stdout.write(self.style.SUCCESS("  Parsing faces"))

            # Parse Keywords
            self.stdout.write(self.style.SUCCESS("  Parsing keywords"))

            # And done
            self.stdout.write(self.style.SUCCESS("  indexing completed"))
