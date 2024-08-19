import logging
from pathlib import Path

from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import db_periodic_task
from huey.contrib.djhuey import db_task
from huey.contrib.djhuey import lock_task

from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.sync import fill_image_metadata_from_db
from scansteward.models import Image as ImageModel

logger = logging.getLogger(__name__)


@db_task()
def sync_metadata_to_files(images: list[ImageModel]) -> None:
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

        except Exception:
            # Log the error with relevant image details
            logger.exception(f"Failed to process metadata for image {image.original_path}")

    if metadata_items:
        bulk_write_image_metadata(metadata_items)
        for image in images:
            image.update_hashes()
            image.mark_as_clean()


@db_task
def index_images(images: list[Path]) -> None:
    pass


@db_periodic_task(crontab(minute="0", hour="*"))
@lock_task("trash-delete")
def remove_trashed_images() -> None:
    # Filter images based on deleted_at being less than now - some set period of time and call .delete on the queryset
    # TODO: Set the days from settings
    qs = ImageModel.objects.filter(deleted_at__lte=timezone.now() - timezone.timedelta(days=30))

    qs.delete()
