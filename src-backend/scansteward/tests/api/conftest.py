import datetime

import pytest
from django.http import HttpResponse
from django.test.client import Client
from faker import Faker

from scansteward.models import Person
from scansteward.models import RoughLocation
from scansteward.tests.api.types import AlbumApiGeneratorProtocol
from scansteward.tests.api.types import LocationGeneratorProtocol
from scansteward.tests.api.types import PersonGeneratorProtocol


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


@pytest.fixture(scope="session")
def today() -> datetime.date:
    return datetime.datetime.now(tz=datetime.timezone.utc).date()
