from scansteward.imageops.constants import DATE_KEYWORD
from scansteward.imageops.models import DimensionsStruct
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import KeywordInfoModel
from scansteward.imageops.models import KeywordStruct
from scansteward.imageops.models import RegionInfoStruct
from scansteward.imageops.models import RegionStruct
from scansteward.imageops.models import RotationEnum
from scansteward.imageops.models import XmpAreaStruct
from scansteward.models import Image as ImageModel
from scansteward.models import PersonInImage
from scansteward.models import PetInImage


def fill_image_metadata_from_db(image: ImageModel, image_metadata: ImageMetadata) -> bool:
    """
    Given a dirty image, constructs a new ImageMetadata object and populates it with the data from the database.

    For use in syncing the database into the image file.
    """

    def _update_description() -> bool:
        if image.description is not None:
            image_metadata.Description = image.description
            return True
        return False

    def _update_orientation() -> bool:
        image_metadata.Orientation = RotationEnum(image.orientation)
        return True

    def _update_region_info() -> bool:
        def _add_people_regions() -> None:
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

        def _add_pets_regions() -> None:
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

        if image.people.count() > 0 or image.pets.count() > 0:
            region_info = RegionInfoStruct(
                AppliedToDimensions=DimensionsStruct(H=float(image.height), W=float(image.width), Unit="pixel"),
                RegionList=[],
            )
            _add_people_regions()
            _add_pets_regions()
            image_metadata.RegionInfo = region_info
            return True
        return False

    def _update_location() -> bool:
        if image.location is not None:
            image_metadata.Country = image.location.country_name
            if image.location.city is not None:
                image_metadata.City = image.location.city
            if image.location.subdivision_name is not None:
                image_metadata.State = image.location.subdivision_name
            if image.location.sub_location is not None:
                image_metadata.Location = image.location.sub_location
            return True
        return False

    def _update_date() -> bool:
        if image.date is not None:
            year_keyword = KeywordStruct(Keyword=str(image.date.date.year))
            month_keyword = None
            if image.date.month_valid:
                month_keyword = KeywordStruct(Keyword=f"{image.date.date.month} - {image.date.date.strftime('%B')}")
                year_keyword.Children.append(month_keyword)
            if image.date.day_valid and month_keyword:
                month_keyword.Children.append(KeywordStruct(Keyword=str(image.date.date.day)))
            image_metadata.KeywordInfo = KeywordInfoModel(
                Hierarchy=[
                    KeywordStruct(
                        Keyword=DATE_KEYWORD,
                        Applied=False,
                        Children=[year_keyword],
                    ),
                ],
            )
            return True
        return False

    def _update_tags() -> bool:
        # TODO: Construct the keywords
        return False

    updated = _update_description()
    updated = _update_orientation() or updated
    updated = _update_region_info() or updated
    updated = _update_location() or updated
    updated = _update_date() or updated
    return _update_tags() or updated
