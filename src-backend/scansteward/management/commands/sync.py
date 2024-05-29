from typing import Annotated

from django_typer import TyperCommand
from typer import Option

from scansteward.models import Image as ImageModel


class Command(TyperCommand):
    help = "Syncs dirty image metadata to the file system"

    def handle(
        self,
        synchronous: Annotated[bool, Option(help="The paths to index for new images")] = True,
    ):
        ImageModel.objects.filter(is_dirty=True)
