from http import HTTPStatus

from django.http import HttpResponse

from scansteward.models import Person
from scansteward.tests.api.utils import FakerTestCase


class GeneratePeopleTestCase(FakerTestCase):
    def generate_people(self, count: int, *, with_description: bool = False) -> None:
        Person.objects.all().delete()
        self.people = []
        for _ in range(count):
            name = self.faker.unique.name()
            description = self.faker.sentence if with_description else None
            self.people.append(Person.objects.create(name=name, description=description))
        assert Person.objects.count() == count


class TestApiPeopleRead(GeneratePeopleTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_get_people_with_no_people(self):
        Person.objects.all().delete()
        resp = self.client.get("/api/person/", headers={"accept": "application/json"})

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == 0
        assert len(data["items"]) == 0

    def test_list_people(self):
        count = 5
        self.generate_people(count)

        resp = self.client.get("/api/person/", headers={"accept": "application/json"})

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == count

    def test_list_people_limit_offset(self):
        count = 5
        limit = 3
        offset = 0
        self.generate_people(count)

        resp = self.client.get(
            f"/api/person/?limit={limit}&offset={offset}",
            headers={"accept": "application/json"},
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == limit


class TestApiPeopleCreate(FakerTestCase):
    def create_single_person(self, name: str, description: str | None = None) -> HttpResponse:
        data = {"name": name}
        if description is not None:
            data.update({"description": description})
        return self.client.post(
            "/api/person/",
            content_type="application/json",
            data=data,
        )

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


class TestApiPeopleUpdate(GeneratePeopleTestCase):
    def test_update_person(self):
        self.generate_people(1)

        instance: Person = self.people[0]

        new_name = self.faker.name()

        resp = self.client.put(
            f"/api/person/{instance.pk}",
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


class TestApiPeopleDelete(GeneratePeopleTestCase):
    def test_delete_person(self):
        self.generate_people(1)

        instance: Person = self.people[0]

        resp = self.client.delete(f"/api/person/{instance.pk}")

        assert resp.status_code == HTTPStatus.NO_CONTENT
