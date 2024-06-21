import logging

from huey.contrib.djhuey import task

from scansteward.models import Image as ImageModel

logger = logging.getLogger(__name__)


@task()
def sync_metadata_to_files(images: list[ImageModel]) -> None:
    pass


async def remove_trashed_images() -> None:
    pass
