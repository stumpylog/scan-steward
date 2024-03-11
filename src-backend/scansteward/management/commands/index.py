from enum import IntEnum
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Final

from blake3 import blake3
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image

from scansteward.imageops.metadata import read_image_metadata
from scansteward.imageops.models import KeywordStruct
from scansteward.models import FaceInImage
from scansteward.models import Image as ImageModel
from scansteward.models import Person
from scansteward.models import Tag


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
            for file_generator in [path.glob(f"**/*{x}") for x in self.IMAGE_EXTENSIONS]:
                for filename in file_generator:
                    self.stdout.write(self.style.SUCCESS(f"Indexing {filename.name}"))
                    self.handle_single_image(filename)

    def handle_single_image(self, image_path: Path) -> None:
        # Duplicate check
        image_hash = blake3(image_path.read_bytes(), max_threads=self.threads).hexdigest()

        # Update or create
        with transaction.atomic():
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
            self.stdout.write(
                self.style.NOTICE(
                    f"  Updating path from {existing_image.original_path.resolve()} to {image_path.resolve()}",
                ),
            )
            existing_image.original_path = image_path.resolve()
            existing_image.save()
        self.stdout.write(self.style.SUCCESS(f"  {image_path.name} indexing completed"))

    def handle_new_image(self, image_path: Path, image_hash: str) -> None:
        new_img = ImageModel.objects.create(
            file_size=image_path.stat().st_size,
            checksum=image_hash,
            original=str(image_path.resolve()),
            source=self.source,
        )

        self.stdout.write(self.style.SUCCESS("  Creating thumbnail"))
        with Image.open(image_path) as im_file:
            img_copy = im_file.copy()
            img_copy.thumbnail((500, 500))
            img_copy.save(new_img.thumbnail_path)

        self.stdout.write(self.style.SUCCESS("  Creating WebP version"))
        with Image.open(image_path) as im_file:
            im_file.save(new_img.full_size_path, quality=90)

        metadata = read_image_metadata(image_path)

        # Parse Faces
        self.stdout.write(self.style.SUCCESS("  Parsing faces"))
        if metadata.RegionInfo:
            for region in metadata.RegionInfo.RegionList:
                if region.Type == "Face" and region.Name:
                    person, _ = Person.objects.get_or_create(name=region.Name)
                    if region.Description:  # pragma: no cover
                        person.description = region.Description
                        person.save()
                    self.stdout.write(self.style.SUCCESS(f"  Found face for {person.name}"))
                    _ = FaceInImage.objects.create(
                        person=person,
                        image=new_img,
                        center_x=region.Area.X,
                        center_y=region.Area.Y,
                        height=region.Area.H,
                        width=region.Area.W,
                    )
                elif region.Type != "Face":  # pragma: no cover
                    self.stdout.write(self.style.SUCCESS(f"  Skipping region of type {region.Type}"))
                elif not region.Name:  # pragma: no cover
                    self.stdout.write(self.style.SUCCESS("  Skipping region with empty Name"))

        # Parse Keywords
        self.stdout.write(self.style.SUCCESS("  Parsing keywords"))
        if metadata.KeywordInfo:

            def maybe_create_tag_tree(image_instance: ImageModel, parent: Tag, tree_node: KeywordStruct):
                existing_node, _ = Tag.objects.get_or_create(name=tree_node.Keyword, parent=parent)
                image_instance.tags.add(existing_node)
                for node_child in tree_node.Children:
                    maybe_create_tag_tree(image_instance, existing_node, node_child)

            for keyword in metadata.KeywordInfo.Hierarchy:
                # Digikam uses this to also store information on people
                # But that is already in the face regions
                if keyword.Keyword == "People":
                    continue
                existing_root_tag, _ = Tag.objects.get_or_create(name=keyword.Keyword, parent=None)
                new_img.tags.add(existing_root_tag)
                for child in keyword.Children:
                    maybe_create_tag_tree(new_img, existing_root_tag, child)
        else:  # pragma: no cover
            self.stdout.write(self.style.SUCCESS("  No keywords"))

        # And done
        self.stdout.write(self.style.SUCCESS("  indexing completed"))
