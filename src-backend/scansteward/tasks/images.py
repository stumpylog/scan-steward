import logging

from django.db import transaction
from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import db_periodic_task
from huey.contrib.djhuey import db_task
from huey.contrib.djhuey import lock_task

from scansteward.imageops.index import handle_existing_image
from scansteward.imageops.index import handle_new_image
from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.sync import fill_image_metadata_from_db
from scansteward.models import Image as ImageModel
from scansteward.tasks.models import ImageIndexTaskModel
from scansteward.utils import calculate_blake3_hash

logger = logging.getLogger(__name__)


@db_task()
def sync_metadata_to_files(images: list[ImageModel]) -> None:
    """
    Syncs the metadata from the database to the image file for the given models

    Models are assumed to be dirty already
    """
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


@db_task()
def index_single_image(pkg: ImageIndexTaskModel) -> None:
    if not pkg.logger:
        pkg.logger = logger

    pkg.logger.info(f"Indexing {pkg.image_path.stem}")

    # Duplicate check
    image_hash = calculate_blake3_hash(pkg.image_path, hash_threads=pkg.hash_threads)

    # Update or create
    with transaction.atomic():
        existing_image = ImageModel.objects.filter(original_checksum=image_hash).first()
        if existing_image is not None:
            handle_existing_image(existing_image, pkg)
        else:
            handle_new_image(pkg)


@db_periodic_task(crontab(minute="0", hour="0"))
@lock_task("trash-delete")
def remove_trashed_images() -> None:
    # Filter images based on deleted_at being less than now - some set period of time and call .delete on the queryset
    # TODO: Set the days from settings
    qs = ImageModel.objects.filter(deleted_at__lte=timezone.now() - timezone.timedelta(days=30))

    qs.delete()
