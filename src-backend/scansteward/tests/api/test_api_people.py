from http import HTTPStatus

import pytest
from django.db import transaction
from django.test import TestCase
from django.test.client import Client
from faker import Faker

from scansteward.models import Person
from scansteward.tests.api.utils import GeneratePeopleMixin
from scansteward.tests.mixins import DirectoriesMixin


def generate_people_objects(faker: Faker, count: int, *, with_description: bool = False) -> None:
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


@pytest.mark.django_db()
class TestApiPeopleRead:
    def test_get_people_with_no_people(self, client: Client):
        Person.objects.all().delete()
        resp = client.get(
            "/api/person/",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == 0
        assert len(data["items"]) == 0

    def test_get_person_does_not_exist(self, client: Client):
        resp = client.get(
            "/api/person/1/",
        )

        assert resp.status_code == HTTPStatus.NOT_FOUND

    def test_get_person_does_exist(self, client: Client, faker: Faker):
        generate_people_objects(faker, 1)
        resp = client.get(
            "/api/person/1/",
        )

        assert resp.status_code == HTTPStatus.OK
        instance = Person.objects.get(pk=1)
        data = resp.json()
        assert "id" in data
        assert data["id"] == instance.pk
        assert "name" in data
        assert data["name"] == instance.name

    def test_list_people(self, client: Client, faker: Faker):
        count = 5
        generate_people_objects(faker, count)

        resp = client.get(
            "/api/person/",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == count

    def test_list_people_limit_offset(self, client: Client, faker: Faker):
        count = 5

        generate_people_objects(faker, count)

        page = 1
        resp = client.get(
            f"/api/person/?page={page}",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == count

        page = 10
        resp = client.get(
            f"/api/person/?page={page}",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == 0


class TestApiPeopleCreate(GeneratePeopleMixin, DirectoriesMixin, TestCase):
    def test_create_person(self, client: Client, faker: Faker):
        person_name = self.faker.name()
        resp = self.create_single_person_via_api(person_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert data["name"] == person_name
        assert "id" in data

        assert Person.objects.filter(id=data["id"]).exists()
        assert Person.objects.get(id=data["id"]).name == person_name

    def test_create_person_with_description(self, client: Client):
        person_name = self.faker.name()
        description = self.faker.sentence()
        resp = self.create_single_person_via_api(person_name, description)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert data["name"] == person_name
        assert "id" in data

        assert Person.objects.filter(id=data["id"]).exists()
        assert Person.objects.get(id=data["id"]).name == person_name
        assert Person.objects.get(id=data["id"]).description == description

    def test_create_multiple_person(self, client: Client):
        count = 5

        for _ in range(count):
            person_name = self.faker.name()
            resp = self.create_single_person_via_api(person_name)

            assert resp.status_code == HTTPStatus.CREATED
            data = resp.json()
            assert data["name"] == person_name
            assert "id" in data

            assert Person.objects.filter(id=data["id"]).exists()
            assert Person.objects.get(id=data["id"]).name == person_name

        assert Person.objects.count() == count

    def test_create_person_existing_name(self, client: Client):
        person_name = self.faker.name()
        resp = self.create_single_person_via_api(person_name)

        assert resp.status_code == HTTPStatus.CREATED

        resp = self.create_single_person_via_api(person_name)
        assert resp.status_code == HTTPStatus.CONFLICT
        assert Person.objects.count() == 1


class TestApiPeopleUpdate(GeneratePeopleMixin, DirectoriesMixin, TestCase):
    def test_update_person_name(self, client: Client):
        generate_people_objects(1)

        instance: Person = self.people[0]

        new_name = self.faker.name()

        resp = client.patch(
            f"/api/person/{instance.pk}/",
            content_type="application/json",
            data={"name": new_name},
        )

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert data["name"] == new_name
        assert "id" in data
        created_id = data["id"]
        assert Person.objects.filter(id=created_id).exists()
        assert Person.objects.get(id=created_id).name == new_name

    def test_update_person_description(self, client: Client):
        generate_people_objects(1)

        instance: Person = self.people[0]

        new_desc = self.faker.sentence()

        resp = client.patch(
            f"/api/person/{instance.pk}/",
            content_type="application/json",
            data={"description": new_desc},
        )

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert data["name"] == instance.name
        assert data["description"] == new_desc


class TestApiPeopleDelete(GeneratePeopleMixin, DirectoriesMixin, TestCase):
    def test_delete_person(self, client: Client):
        generate_people_objects(1)

        instance: Person = self.people[0]

        resp = client.delete(f"/api/person/{instance.pk}/")

        assert resp.status_code == HTTPStatus.NO_CONTENT
