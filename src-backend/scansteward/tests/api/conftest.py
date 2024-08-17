import datetime

import pytest
from django.http import HttpResponse
from django.test.client import Client
from faker import Faker

from scansteward.models import Album
from scansteward.models import Person
from scansteward.models import Pet
from scansteward.models import RoughDate
from scansteward.models import RoughLocation
from scansteward.models import Tag
from scansteward.tests.api.types import AlbumApiGeneratorProtocol
from scansteward.tests.api.types import AlbumGeneratorProtocol
from scansteward.tests.api.types import ChildTagGeneratorProtocol
from scansteward.tests.api.types import DateGeneratorProtocol
from scansteward.tests.api.types import LocationGeneratorProtocol
from scansteward.tests.api.types import PersonGeneratorProtocol
from scansteward.tests.api.types import PetApiGeneratorProtocol
from scansteward.tests.api.types import PetGeneratorProtocol
from scansteward.tests.api.types import TagGeneratorProtocol


@pytest.fixture()
def album_db_factory(faker: Faker) -> AlbumGeneratorProtocol:
    """
    Fixture to return a factory function which generates people directly in the database
    """

    def generate_album_objects(*, with_description: bool = False) -> int:
        """
        Directly generate Person objects into the database
        """
        name = faker.unique.name()
        description = faker.sentence if with_description else None
        o = Album.objects.create(name=name, description=description)
        return o.pk

    return generate_album_objects


@pytest.fixture()
def album_api_create_factory(client: Client, faker: Faker) -> AlbumApiGeneratorProtocol:
    def create_single_album(name: str | None = None, description: str | None = None) -> HttpResponse:
        if name is None:
            name = faker.unique.name()
        data = {"name": name}
        if description is not None:
            data.update({"description": description})
        return client.post(
            "/api/album/",
            content_type="application/json",
            data=data,
        )

    return create_single_album


@pytest.fixture()
def person_db_factory(faker: Faker) -> PersonGeneratorProtocol:
    """
    Fixture to return a factory function which generates people directly in the database
    """

    def generate_people_objects(*, with_description: bool = False) -> int:
        """
        Directly generate Person objects into the database
        """
        name = faker.unique.name()
        description = faker.sentence if with_description else None
        o = Person.objects.create(name=name, description=description)
        return o.pk

    return generate_people_objects


@pytest.fixture()
def location_db_factory(faker: Faker) -> LocationGeneratorProtocol:
    """
    Fixture to return a factory function which generates locations directly in the database
    """

    def create_single_location_object(
        country: str,
        subdivision: str | None = None,
        city: str | None = None,
        location: str | None = None,
    ) -> int:
        instance = RoughLocation.objects.create(
            country_code=country,
            subdivision_code=subdivision,
            city=city,
            sub_location=location,
        )
        return instance.pk

    return create_single_location_object


@pytest.fixture()
def date_db_factory(faker: Faker) -> DateGeneratorProtocol:
    """
    Fixture to return a factory function which generates locations directly in the database
    """

    def create_single_rough_date_object() -> int:
        date = faker.date_this_century()
        month_valid = faker.pybool()
        day_valid = faker.pybool() if month_valid else False
        o = RoughDate.objects.create(date=date, month_valid=month_valid, day_valid=day_valid)
        return o.pk

    return create_single_rough_date_object


@pytest.fixture()
def pet_db_factory(faker: Faker) -> PetGeneratorProtocol:
    """
    Fixture to return a factory function which generates pets directly in the database
    """

    def generate_pet_object(*, with_description: bool = False) -> int:
        """
        Directly generate Person objects into the database
        """
        name = faker.unique.name()
        description = faker.sentence if with_description else None
        o = Pet.objects.create(name=name, description=description)
        return o.pk

    return generate_pet_object


@pytest.fixture()
def pet_api_create_factory(client: Client, faker: Faker) -> PetApiGeneratorProtocol:
    def create_single_pet(name: str | None = None, description: str | None = None) -> HttpResponse:
        if name is None:
            name = faker.unique.name()
        data = {"name": name}
        if description is not None:
            data.update({"description": description})
        return client.post(
            "/api/pet/",
            content_type="application/json",
            data=data,
        )

    return create_single_pet


@pytest.fixture()
def root_tag_db_factory(faker: Faker) -> TagGeneratorProtocol:
    """
    Fixture to return a factory function which generates people directly in the database
    """

    def generate_root_tag_objects(*, with_description: bool = False) -> None:
        """
        Directly create root Tag objects into the database
        """
        name = faker.unique.word()
        description = faker.sentence if with_description else None
        o = Tag.objects.create(name=name, description=description)
        return o.pk

    return generate_root_tag_objects


@pytest.fixture()
def child_tag_db_factory(faker: Faker) -> ChildTagGeneratorProtocol:
    """ """

    def generate_child_tag_objects(parent_id: int, *, with_description: bool = False) -> int:
        """
        Directly create child Tags under the given parent ID
        """
        parent = Tag.objects.get(id=parent_id)
        name = faker.unique.word()
        description = faker.sentence if with_description else None
        o = Tag.objects.create(name=name, description=description, parent=parent)
        return o.pk

    return generate_child_tag_objects


@pytest.fixture(scope="session")
def date_today_utc() -> datetime.date:
    return datetime.datetime.now(tz=datetime.UTC).date()
