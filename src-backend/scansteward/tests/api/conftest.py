from typing import Protocol

import pytest
from django.db import transaction
from faker import Faker

from scansteward.models import Person


class PersonGeneratorProtocol(Protocol):
    def __call__(self, count: int, *, with_description: bool = False) -> None:
        pass


@pytest.fixture()
def person_db_factory(faker: Faker) -> PersonGeneratorProtocol:
    """
    Fixture to return a factory function which generates people directly in the database
    """

    def generate_people_objects(count: int, *, with_description: bool = False) -> None:
        """
        Directly generate Person objects into the database
        """
        with transaction.atomic():
            Person.objects.all().delete()
            for _ in range(count):
                name = faker.unique.name()
                description = faker.sentence if with_description else None
                Person.objects.create(name=name, description=description)

            assert Person.objects.count() == count

    return generate_people_objects
