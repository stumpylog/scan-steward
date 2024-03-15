from http import HTTPStatus

from django.test import TestCase

from scansteward.models import Person
from scansteward.tests.api.utils import GeneratePeopleMixin
from scansteward.tests.mixins import DirectoriesMixin


class TestApiPeopleRead(GeneratePeopleMixin, DirectoriesMixin, TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_get_people_with_no_people(self):
        Person.objects.all().delete()
        resp = self.client.get(
            "/api/person/",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == 0
        assert len(data["items"]) == 0

    def test_get_person_does_not_exist(self):
        resp = self.client.get(
            "/api/person/1/",
        )

        assert resp.status_code == HTTPStatus.NOT_FOUND

    def test_get_person_does_exist(self):
        self.generate_people_objects(1)
        resp = self.client.get(
            "/api/person/1/",
        )

        assert resp.status_code == HTTPStatus.OK
        instance: Person = self.people[0]
        data = resp.json()
        assert "id" in data
        assert data["id"] == instance.pk
        assert "name" in data
        assert data["name"] == instance.name

    def test_list_people(self):
        count = 5
        self.generate_people_objects(count)

        resp = self.client.get(
            "/api/person/",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == count

    def test_list_people_limit_offset(self):
        count = 5
        limit = 3
        offset = 0
        self.generate_people_objects(count)

        resp = self.client.get(
            f"/api/person/?limit={limit}&offset={offset}",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == limit


class TestApiPeopleCreate(GeneratePeopleMixin, DirectoriesMixin, TestCase):

    def test_create_person(self):
        person_name = self.faker.name()
        resp = self.create_single_person_via_api(person_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert data["name"] == person_name
        assert "id" in data

        assert Person.objects.filter(id=data["id"]).exists()
        assert Person.objects.get(id=data["id"]).name == person_name

    def test_create_person_with_description(self):
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

    def test_create_multiple_person(self):

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

    def test_create_person_existing_name(self):
        person_name = self.faker.name()
        resp = self.create_single_person_via_api(person_name)

        assert resp.status_code == HTTPStatus.CREATED

        resp = self.create_single_person_via_api(person_name)
        assert resp.status_code == HTTPStatus.BAD_REQUEST
        assert Person.objects.count() == 1


class TestApiPeopleUpdate(GeneratePeopleMixin, DirectoriesMixin, TestCase):
    def test_update_person_name(self):
        self.generate_people_objects(1)

        instance: Person = self.people[0]

        new_name = self.faker.name()

        resp = self.client.patch(
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

    def test_update_person_description(self):
        self.generate_people_objects(1)

        instance: Person = self.people[0]

        new_desc = self.faker.sentence()

        resp = self.client.patch(
            f"/api/person/{instance.pk}/",
            content_type="application/json",
            data={"description": new_desc},
        )

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert data["name"] == instance.name
        assert data["description"] == new_desc


class TestApiPeopleDelete(GeneratePeopleMixin, DirectoriesMixin, TestCase):
    def test_delete_person(self):
        self.generate_people_objects(1)

        instance: Person = self.people[0]

        resp = self.client.delete(f"/api/person/{instance.pk}/")

        assert resp.status_code == HTTPStatus.NO_CONTENT
