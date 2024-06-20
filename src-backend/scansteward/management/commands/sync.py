from typing import Annotated

from django.core.paginator import Paginator
from django_typer import TyperCommand
from typer import Option

from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.models import DimensionsStruct
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import KeywordInfoModel
from scansteward.imageops.models import KeywordStruct
from scansteward.imageops.models import RegionInfoStruct
from scansteward.imageops.models import RegionStruct
from scansteward.imageops.models import RotationEnum
from scansteward.imageops.models import XmpAreaStruct
from scansteward.management.commands.mixins import ImageHasherMixin
from scansteward.management.commands.mixins import KeywordNameMixin
from scansteward.models import Image as ImageModel
from scansteward.models import PersonInImage
from scansteward.models import PetInImage


class Command(KeywordNameMixin, ImageHasherMixin, TyperCommand):
    help = "Syncs dirty image metadata to the file system"

    def handle(
        self,
        synchronous: Annotated[bool, Option(help="If True, run the writing in the same process")] = True,
    ):
        paginator = Paginator(
            ImageModel.objects.filter(is_dirty=True)
            .filter(in_trash=False)
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
            updated = False
            metadata = ImageMetadata(SourceFile=image.original_path, ImageHeight=image.height, ImageWidth=image.width)

            if image.description is not None:
                updated = True
                metadata.Description = image.description

            if image.orientation is not None:
                updated = True
                metadata.Orientation = RotationEnum(image.orientation)

            if image.people.count() > 0 or image.pets.count() > 0:
                updated = True
                region_info = RegionInfoStruct(
                    AppliedToDimensions=DimensionsStruct(H=float(image.height), W=float(image.width), Unit="pixel"),
                    RegionList=[],
                )
                for person in image.people.all():
                    person_box = PersonInImage.objects.filter(image=image, person=person).get()
                    region_info.RegionList.append(
                        RegionStruct(
                            Name=person.name,
                            Type="Face",
                            Area=XmpAreaStruct(
                                H=person_box.height,
                                W=person_box.width,
                                X=person_box.center_x,
                                Y=person_box.center_y,
                                Unit="normalized",
                            ),
                            Description=person.description,
                        ),
                    )
                for pet in image.pets.all():
                    pet_box = PetInImage.objects.filter(image=image, pet=pet).get()
                    region_info.RegionList.append(
                        RegionStruct(
                            Name=pet.name,
                            Type="Pet",
                            Area=XmpAreaStruct(
                                H=pet_box.height,
                                W=pet_box.width,
                                X=pet_box.center_x,
                                Y=pet_box.center_y,
                                Unit="normalized",
                            ),
                            Description=pet_box.description,
                        ),
                    )

            # Location is NOT synced into the tags, it uses the MWG values instead
            if image.location is not None:
                updated = True
                metadata.Country = image.location.country_name
                if image.location.city is not None:
                    metadata.City = image.location.city
                if image.location.subdivision_name is not None:
                    metadata.State = image.location.subdivision_name
                if image.location.sub_location is not None:
                    metadata.Location = image.location.sub_location

            # Date
            if image.date is not None:
                updated = True
                # The year will always be valid
                year_keyword = KeywordStruct(Keyword=str(image.date.date.year))
                month_keyword = None

                # If possible, store the month
                if image.date.month_valid:
                    # Include the number (for sorting) and the full name
                    month_keyword = KeywordStruct(Keyword=f"{image.date.date.month} - {image.date.date.strftime('%B')}")
                    year_keyword.Children.append(month_keyword)

                # If possible, store the day
                # month_keyword will always be set, its checked mostly for typing
                if image.date.day_valid and month_keyword:
                    month_keyword.Children.append(KeywordStruct(Keyword=str(image.date.date.day)))

                metadata.KeywordInfo = KeywordInfoModel(
                    Hierarchy=[
                        KeywordStruct(
                            Keyword=self.DATE_KEYWORD,
                            Applied=False,
                            Children=[year_keyword],
                        ),
                    ],
                )

            # TODO: Tags via KeywordStruct

            if updated:
                metadata_items.append(metadata)

        if metadata_items:
            bulk_write_image_metadata(metadata_items)
            for image in images:
                self.update_image_hash(image)
                image.mark_as_clean()
