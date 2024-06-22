import datetime
from typing import Protocol

import pytest
from faker import Faker

from scansteward.models import Person
from scansteward.models import RoughLocation


class PersonGeneratorProtocol(Protocol):
    def __call__(self, *, with_description: bool = False) -> int:  # type: ignore[return]
        pass


class LocationGeneratorProtocol(Protocol):
    def __call__(
        self,
        country: str,
        subdivision: str | None = None,
        city: str | None = None,
        location: str | None = None,
    ) -> int:  # type: ignore[return]
        pass


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

    def util_create_location_object(
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

    return util_create_location_object


@pytest.fixture(scope="session")
def today() -> datetime.date:
    return datetime.datetime.now(tz=datetime.timezone.utc).date()
