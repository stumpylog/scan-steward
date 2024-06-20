import random
from typing import TYPE_CHECKING

from django.http import HttpResponse
from faker import Faker

from scansteward.models import Image
from scansteward.models import Person
from scansteward.models import Pet
from scansteward.models import RoughDate
from scansteward.models import Tag

if TYPE_CHECKING:
    from django.test.client import Client


class FakerMixin:
    def setUp(self) -> None:
        self.faker = Faker()
        if TYPE_CHECKING:
            assert hasattr(self, "setUp")
            assert callable(self.setUp)
        return super().setUp()


class GenerateTagsMixin(FakerMixin):
    def setUp(self) -> None:
        self.roots: list[Tag] = []
        self.children: list[Tag] = []
        return super().setUp()

    def generate_root_tag_objects(self, count: int, *, with_description: bool = False) -> None:
        """
        Directly create root Tag objects into the database
        """
        Tag.objects.all().delete()
        for _ in range(count):
            name = self.faker.unique.word()
            description = self.faker.sentence if with_description else None
            self.roots.append(Tag.objects.create(name=name, description=description))

    def generate_child_tag_object(self, count: int, parent_id: int, *, with_description: bool = False):
        """
        Directly create child Tags under the given parent ID
        """
        parent = Tag.objects.get(id=parent_id)
        for _ in range(count):
            name = self.faker.unique.word()
            description = self.faker.sentence if with_description else None
            self.children.append(Tag.objects.create(name=name, description=description, parent=parent))


class GeneratePeopleMixin(FakerMixin):
    def setUp(self) -> None:
        self.people: list[Person] = []
        return super().setUp()

    def create_single_person_via_api(self, name: str, description: str | None = None) -> HttpResponse:
        """
        Creates a Person via the API
        """
        data = {"name": name}
        if description is not None:
            data.update({"description": description})
        if TYPE_CHECKING:
            assert hasattr(self, "client")
            assert isinstance(self.client, Client)
        return self.client.post(
            "/api/person/",
            content_type="application/json",
            data=data,
        )

    def generate_people_objects(self, count: int, *, with_description: bool = False) -> None:
        """
        Directly generate Person objects into the database
        """
        Person.objects.all().delete()
        for _ in range(count):
            name = self.faker.unique.name()
            description = self.faker.sentence if with_description else None
            self.people.append(Person.objects.create(name=name, description=description))
        assert Person.objects.count() == count


class GeneratePetsMixin(FakerMixin):
    def setUp(self) -> None:
        self.pets: list[Pet] = []
        return super().setUp()

    def create_single_pet_via_api(self, name: str, description: str | None = None) -> HttpResponse:
        """
        Creates a Person via the API
        """
        data = {"name": name}
        if description is not None:
            data.update({"description": description})
        if TYPE_CHECKING:
            assert hasattr(self, "client")
            assert isinstance(self.client, Client)
        return self.client.post(
            "/api/pet/",
            content_type="application/json",
            data=data,
        )

    def generate_pet_objects(self, count: int, *, with_description: bool = False) -> None:
        """
        Directly generate Pet objects into the database
        """
        Pet.objects.all().delete()
        for _ in range(count):
            name = self.faker.unique.name()
            description = self.faker.sentence if with_description else None
            self.pets.append(Pet.objects.create(name=name, description=description))
        assert Pet.objects.count() == count


class GenerateImagesMixin(FakerMixin):
    def setUp(self) -> None:
        self.images: list[Image] = []
        return super().setUp()

    def create_single_image_via_api(self) -> HttpResponse:
        """
        Creates an Image via the API
        """
        raise NotImplementedError

    def generate_image_objects(self, count: int) -> None:
        """
        Directly generate Image objects into the database
        """
        Image.objects.all().delete()
        for _ in range(count):
            self.images.append(
                Image.objects.create(
                    file_size=random.randint(1, 1_000_000),  # noqa: S311
                    original_checksum=self.faker.sha1()[:64],
                    thumbnail_checksum=self.faker.sha1()[:64],
                    full_size_checksum=self.faker.sha1()[:64],
                    phash=self.faker.sha1()[:64],
                    original=self.faker.file_path(category="image"),
                    height=random.randint(100, 200),  # noqa: S311
                    width=random.randint(100, 200),  # noqa: S311
                ),
            )
        assert Image.objects.count() == count


class GenerateRoughDateMixin(FakerMixin):
    def setUp(self) -> None:
        self.dates: list[RoughDate] = []
        return super().setUp()

    def generate_rough_dates(self, count: int) -> None:
        for _ in range(count):
            date = self.faker.date_this_century()
            month_valid = self.faker.pybool()
            day_valid = self.faker.pybool() if month_valid else False
            self.dates.append(
                RoughDate.objects.create(date=date, month_valid=month_valid, day_valid=day_valid),
            )
