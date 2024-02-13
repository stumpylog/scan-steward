from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase
from faker import Faker

from scansteward.models import Person


class TestApiPeople(TestCase):

    def setUp(self) -> None:
        self.faker = Faker()
        return super().setUp()

    def create_single_person(self, name: str, description: str | None = None) -> HttpResponse:
        data = {"name": name}
        if description is not None:
            data.update({"description": description})
        return self.client.post(
            "/api/person/",
            content_type="application/json",
            data=data,
        )

    def test_get_people_with_no_people(self):
        resp = self.client.get("/api/person/", headers={"accept": "application/json"})

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == 0
        assert len(data["items"]) == 0

    def test_create_person(self):
        person_name = self.faker.name()
        resp = self.create_single_person(person_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert data["name"] == person_name
        assert "id" in data

        assert Person.objects.filter(id=data["id"]).exists()
        assert Person.objects.get(id=data["id"]).name == person_name

    def test_create_person_with_description(self):
        person_name = self.faker.name()
        description = self.faker.sentence()
        resp = self.create_single_person(person_name, description)

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
            resp = self.create_single_person(person_name)

            assert resp.status_code == HTTPStatus.CREATED
            data = resp.json()
            assert data["name"] == person_name
            assert "id" in data

            assert Person.objects.filter(id=data["id"]).exists()
            assert Person.objects.get(id=data["id"]).name == person_name

        assert Person.objects.count() == count

    def test_list_people(self):
        count = 5
        id_to_name = {}

        for _ in range(count):
            person_name = self.faker.name()
            resp = self.create_single_person(person_name)

            assert resp.status_code == HTTPStatus.CREATED

            id_to_name[resp.json()["id"]] = person_name

        assert Person.objects.count() == count

        resp = self.client.get("/api/person/", headers={"accept": "application/json"})

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == count

    def test_update_person(self):
        person_name = self.faker.name()
        resp = self.create_single_person(person_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert data["name"] == person_name
        assert "id" in data
        created_id = data["id"]

        assert Person.objects.filter(id=created_id).exists()
        assert Person.objects.get(id=created_id).name == person_name

        new_name = self.faker.name()

        resp = self.client.put(
            f"/api/person/{created_id}",
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
