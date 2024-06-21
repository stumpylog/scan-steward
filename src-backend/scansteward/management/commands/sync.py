import logging
from typing import Annotated

from django.core.paginator import Paginator
from django_typer import TyperCommand
from typer import Option

from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.sync import fill_image_metadata_from_db
from scansteward.management.commands.mixins import ImageHasherMixin
from scansteward.management.commands.mixins import KeywordNameMixin
from scansteward.models import Image as ImageModel

logger = logging.getLogger(__name__)


class Command(KeywordNameMixin, ImageHasherMixin, TyperCommand):
    help = "Syncs dirty image metadata to the file system"

    def handle(
        self,
        synchronous: Annotated[bool, Option(help="If True, run the writing in the same process")] = True,
    ):
        paginator = Paginator(
            ImageModel.objects.filter(is_dirty=True)
            .filter(in_trash=False)
            .order_by("pk")
            .prefetch_related("location", "date", "people", "pets", "tags")
            .all(),
            10,
        )

        for i in paginator.page_range:
            data_chunk: list[ImageModel] = list(paginator.page(i).object_list)
            self.write_image_metadata(data_chunk)

    def write_image_metadata(self, images: list[ImageModel]) -> None:
        metadata_items = []
        for image in images:
            try:
                metadata = ImageMetadata(
                    SourceFile=image.original_path,
                    ImageHeight=image.height,
                    ImageWidth=image.width,
                )

                updated = fill_image_metadata_from_db(image, metadata)

                if updated:
                    metadata_items.append(metadata)

            except Exception:  # noqa: PERF203
                # Log the error with relevant image details
                logger.exception(f"Failed to process metadata for image {image.original_path}")

        if metadata_items:
            bulk_write_image_metadata(metadata_items)
            for image in images:
                self.update_image_hash(image)
                image.mark_as_clean()
