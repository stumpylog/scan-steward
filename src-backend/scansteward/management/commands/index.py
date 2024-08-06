from datetime import date
from pathlib import Path
from typing import Annotated
from typing import Final
from typing import Optional

from django.db import transaction
from django_typer.management import TyperCommand
from PIL import Image
from typer import Argument
from typer import Option

from scansteward.imageops.metadata import read_image_metadata
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import KeywordStruct
from scansteward.management.commands.mixins import ImageHasherMixin
from scansteward.management.commands.mixins import KeywordNameMixin
from scansteward.models import Image as ImageModel
from scansteward.models import ImageSource
from scansteward.models import Person
from scansteward.models import PersonInImage
from scansteward.models import Pet
from scansteward.models import PetInImage
from scansteward.models import RoughDate
from scansteward.models import RoughLocation
from scansteward.models import Tag
from scansteward.routes.locations.utils import get_country_code_from_name
from scansteward.routes.locations.utils import get_subdivision_code_from_name


class Command(KeywordNameMixin, ImageHasherMixin, TyperCommand):
    help = "Indexes the given path(s) for new Images"

    IMAGE_EXTENSIONS: Final[set[str]] = {
        ".jpg",
        ".jpeg",
        ".png",
        ".tiff",
        ".tif",
        ".webp",
    }

    def handle(
        self,
        paths: Annotated[list[Path], Argument(help="The paths to index for new images")],
        hash_threads: Annotated[int, Option(help="Number of threads to use for hashing")] = 2,
        source: Annotated[
            Optional[str],  # noqa: UP007
            Option(help="The source of the images to attach to the image"),
        ] = None,
    ) -> None:
        if source:
            self.source, _ = ImageSource.objects.get_or_create(name=source)
        else:
            self.source = None

        self.hash_threads = hash_threads

        for path in paths:
            for file_generator in [path.glob(f"**/*{x}") for x in self.IMAGE_EXTENSIONS]:
                for filename in file_generator:
                    self.stdout.write(self.style.SUCCESS(f"Indexing {filename.name}"))
                    try:
                        self.handle_single_image(filename)
                    except KeyboardInterrupt:
                        break

    def handle_single_image(self, image_path: Path) -> None:
        """
        Handles indexing a single image, either existing or new
        """
        # Duplicate check
        image_hash = self.hash_file(image_path, hash_threads=self.hash_threads)

        # Update or create
        with transaction.atomic():
            existing_image = ImageModel.objects.filter(original_checksum=image_hash).first()
            if existing_image is not None:
                self.handle_existing_image(existing_image, image_path)
            else:
                self.handle_new_image(image_path)

    def handle_existing_image(
        self,
        existing_image: ImageModel,
        image_path: Path,
    ) -> None:
        """
        Handles an image that has already been indexed, either updating its source or changing the location
        """
        self.stdout.write(self.style.NOTICE("  Image already indexed"))
        # Set the source if requested
        if self.source is not None and (existing_image.source is None or existing_image.source != self.source):
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

    def handle_new_image(self, image_path: Path) -> None:
        """
        Handles a completely new image
        """
        metadata = read_image_metadata(image_path)

        new_img = ImageModel.objects.create(
            file_size=image_path.stat().st_size,
            original=str(image_path.resolve()),
            source=self.source,
            orientation=metadata.Orientation or ImageModel.OrientationChoices.HORIZONTAL,
            description=metadata.Description,
            height=metadata.ImageHeight,
            width=metadata.ImageWidth,
            # These are placeholders
            original_checksum="A",
            thumbnail_checksum="B",
            full_size_checksum="C",
            phash="D",
            # This time cannot be dirty
            is_dirty=False,
        )

        self.stdout.write(self.style.SUCCESS("  Creating thumbnail"))
        with Image.open(image_path) as im_file:
            img_copy = im_file.copy()
            img_copy.thumbnail((500, 500))
            img_copy.save(new_img.thumbnail_path)

        self.stdout.write(self.style.SUCCESS("  Creating WebP version"))
        with Image.open(image_path) as im_file:
            im_file.save(new_img.full_size_path, quality=90)

        # Update the file hashes, now that the files exist
        self.update_image_hash(new_img, hash_threads=self.hash_threads)

        # Parse Faces/pets/regions
        self.parse_region_info(new_img, metadata)

        # Parse Keywords
        self.parse_keywords(new_img, metadata)

        # Parse Location
        self.parse_location(new_img, metadata)
        if not new_img.location:
            self.parse_location_from_keywords(new_img, metadata)

        # Parse date information from keywords?
        self.parse_dates_from_keywords(new_img, metadata)

        # And done.  Image cannot be dirty, use update to avoid getting marked as such
        new_img.mark_as_clean()
        self.stdout.write(self.style.SUCCESS("  indexing completed"))

    def parse_region_info(self, new_image: ImageModel, metadata: ImageMetadata):
        """
        Parses the MWG regions into people and pets
        """
        self.stdout.write(self.style.SUCCESS("  Parsing regions"))
        if metadata.RegionInfo:
            for region in metadata.RegionInfo.RegionList:
                if region.Type == "Face" and region.Name:
                    person, _ = Person.objects.get_or_create(name=region.Name)
                    if region.Description:
                        person.description = region.Description
                        person.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"  Found face for person {person.name}"),
                    )
                    _ = PersonInImage.objects.create(
                        person=person,
                        image=new_image,
                        center_x=region.Area.X,
                        center_y=region.Area.Y,
                        height=region.Area.H,
                        width=region.Area.W,
                    )
                elif region.Type == "Pet" and region.Name:
                    pet, _ = Pet.objects.get_or_create(name=region.Name)
                    if region.Description:
                        pet.description = region.Description
                        pet.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"  Found box for pet {pet.name}"),
                    )
                    _ = PetInImage.objects.create(
                        pet=pet,
                        image=new_image,
                        center_x=region.Area.X,
                        center_y=region.Area.Y,
                        height=region.Area.H,
                        width=region.Area.W,
                    )
                elif not region.Name:  # pragma: no cover
                    self.stdout.write(
                        self.style.SUCCESS("  Skipping region with empty Name"),
                    )
                elif region.Type not in {"Face", "Pet"}:  # pragma: no cover
                    self.stdout.write(
                        self.style.SUCCESS(f"  Skipping region of type {region.Type}"),
                    )

    def parse_keywords(self, new_image: ImageModel, metadata: ImageMetadata):
        """
        Creates database Tags from the MWG keyword struct
        """
        self.stdout.write(self.style.SUCCESS("  Parsing keywords"))
        if metadata.KeywordInfo:

            def maybe_create_tag_tree(
                image_instance: ImageModel,
                parent: Tag,
                tree_node: KeywordStruct,
            ):
                existing_node, _ = Tag.objects.get_or_create(
                    name=tree_node.Keyword,
                    parent=parent,
                    applied=tree_node.Applied or not tree_node.Children,
                )
                # If this is applied or there are no children, tag it
                if existing_node.applied or not tree_node.Children:
                    image_instance.tags.add(existing_node)
                for node_child in tree_node.Children:
                    maybe_create_tag_tree(image_instance, existing_node, node_child)

            for keyword in metadata.KeywordInfo.Hierarchy:
                # Skip keywords with dedicated processing
                if keyword.Keyword.lower() in {
                    self.PEOPLE_KEYWORD.lower(),
                    self.DATE_KEYWORD.lower(),
                    self.LOCATION_KEYWORD.lower(),
                }:
                    continue
                existing_root_tag, _ = Tag.objects.get_or_create(
                    name=keyword.Keyword,
                    parent=None,
                    applied=False if keyword.Applied is None else keyword.Applied,
                )

                if keyword.Applied or not keyword.Children:
                    new_image.tags.add(existing_root_tag)
                for child in keyword.Children:
                    maybe_create_tag_tree(new_image, existing_root_tag, child)
        else:  # pragma: no cover
            self.stdout.write(self.style.SUCCESS("  No keywords"))

    def parse_location(self, new_image: ImageModel, metadata: ImageMetadata):
        """
        Creates a RoughLocation from a given ImageMetadata object and adds it to the given image.
        """
        if metadata.Country:
            country_alpha_2 = get_country_code_from_name(metadata.Country)
            if country_alpha_2:
                self.stdout.write(
                    self.style.SUCCESS(f"  Got country {country_alpha_2} from {metadata.Country}"),
                )
                subdivision_code = None
                if metadata.State:
                    subdivision_code = get_subdivision_code_from_name(
                        country_alpha_2,
                        metadata.State,
                    )
                    if not subdivision_code:
                        self.stdout.write(
                            self.style.WARNING(f"  No subdivision code found from {metadata.State}"),
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"  Got subdivision code {subdivision_code} from {metadata.State}",
                            ),
                        )
                location, _ = RoughLocation.objects.get_or_create(
                    country_code=country_alpha_2,
                    subdivision_code=subdivision_code,
                    city=metadata.City,
                    sub_location=metadata.Location,
                )
                new_image.location = location
                new_image.save()
                self.stdout.write(self.style.SUCCESS(f"  Location is {location}"))
            else:
                self.stdout.write(self.style.WARNING(f"  No country code found from {metadata.Country}"))
        else:  # pragma: no cover
            self.stdout.write(self.style.SUCCESS("  No country set, will try keywords"))

    def parse_location_from_keywords(self, new_image: ImageModel, metadata: ImageMetadata):
        """
        If the MWG location information is not set, attempts to parse from the keywords

        Looks for a keyword structure like:
        - Locations
          - Country Name
            - Subdivision Name
                - City Name
                    - Sub-location Name

        If the subdivison doesn't match anything within the country, it is assumed to be a city instead

        """
        if (
            metadata.KeywordInfo
            and (location_tree := metadata.KeywordInfo.get_root_by_name(self.LOCATION_KEYWORD))
            and location_tree
            and location_tree.Children
        ):
            country_node = location_tree.Children[0]
            country_alpha2 = get_country_code_from_name(country_node.Keyword)
            if country_alpha2:
                subdivision_code = None
                city = None
                location = None
                if len(country_node.Children) > 0:
                    subdivision_node = country_node.Children[0]
                    subdivision_code = get_subdivision_code_from_name(
                        country_alpha2,
                        subdivision_node.Keyword,
                    )
                    if not subdivision_code:
                        # Assume this is a city instead
                        city = subdivision_node.Keyword
                    elif len(subdivision_node.Children) > 0:
                        # If possible, use the first child as the city
                        city_node = subdivision_node.Children[0]
                        city = city_node.Keyword
                        if len(city_node.Children) > 0:
                            location = city_node.Children[0].Keyword

                location, _ = RoughLocation.objects.get_or_create(
                    country_code=country_alpha2,
                    subdivision_code=subdivision_code,
                    city=city,
                    sub_location=location,
                )
                new_image.location = location
                new_image.save()
                self.stdout.write(self.style.SUCCESS(f"  RoughLocation is {location}"))

    def parse_dates_from_keywords(self, new_image: ImageModel, metadata: ImageMetadata):
        """
        Looks for a keyword structure like:
        - Dates and Times
          - 1980
            - 12 - December
                - 25

        Which will convert into a date like: 1980-12-25

        If no month is found, no day will be looked for.  It is possible to have a rough date of just a year,
        just a month and year or a year, month, day fully built
        """

        if (
            metadata.KeywordInfo
            and metadata.KeywordInfo
            and (date_and_time_tree := metadata.KeywordInfo.get_root_by_name(self.DATE_KEYWORD))
            and len(date_and_time_tree.Children) > 0
        ):
            year_node = date_and_time_tree.Children[0]
            month = 1
            month_valid = False
            day = 1
            day_valid = False
            if len(year_node.Children) > 0:
                month_node = year_node.Children[0]
                day = 1
                day_valid = False
                if len(month_node.Children) > 0:
                    day_node = month_node.Children[0]
                    try:
                        day = int(day_node.Keyword)
                        day_valid = True
                    except ValueError:
                        pass
                try:
                    month = int(month_node.Keyword.split("-")[0])
                    month_valid = True
                except ValueError:
                    pass
            try:
                year = int(year_node.Keyword)

                rough_date, _ = RoughDate.objects.get_or_create(
                    date=date(year=year, month=month, day=day),
                    month_valid=month_valid,
                    day_valid=day_valid,
                )
                self.stdout.write(self.style.SUCCESS(f"  Set rough date of {rough_date}"))
                new_image.date = rough_date
                new_image.save()
            except ValueError:
                pass
