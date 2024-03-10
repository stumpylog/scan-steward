from typing import TYPE_CHECKING

from django.http import HttpResponse
from faker import Faker

from scansteward.models import Person
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
        self.roots = []
        self.children = []
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
        self.people = []
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
