from http import HTTPStatus

from django.test import TestCase

from scansteward.models import Pet
from scansteward.tests.api.utils import GeneratePetsMixin
from scansteward.tests.mixins import DirectoriesMixin


class TestApiPetsRead(GeneratePetsMixin, DirectoriesMixin, TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_get_people_with_no_people(self):
        Pet.objects.all().delete()
        resp = self.client.get(
            "/api/pet/",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == 0
        assert len(data["items"]) == 0

    def test_get_pet_does_not_exist(self):
        resp = self.client.get(
            "/api/pet/1/",
        )

        assert resp.status_code == HTTPStatus.NOT_FOUND

    def test_get_pet_does_exist(self):
        self.generate_pet_objects(1)
        resp = self.client.get(
            "/api/pet/1/",
        )

        assert resp.status_code == HTTPStatus.OK
        instance: Pet = self.pets[0]
        data = resp.json()
        assert "id" in data
        assert data["id"] == instance.pk
        assert "name" in data
        assert data["name"] == instance.name

    def test_list_people(self):
        count = 5
        self.generate_pet_objects(count)

        resp = self.client.get(
            "/api/pet/",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == count

    def test_list_people_limit_offset(self):
        count = 5
        limit = 3
        offset = 0
        self.generate_pet_objects(count)

        resp = self.client.get(
            f"/api/pet/?limit={limit}&offset={offset}",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == limit


class TestApiPetsCreate(GeneratePetsMixin, DirectoriesMixin, TestCase):

    def test_create_pet(self):
        pet_name = self.faker.name()
        resp = self.create_single_pet_via_api(pet_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert data["name"] == pet_name
        assert "id" in data

        assert Pet.objects.filter(id=data["id"]).exists()
        assert Pet.objects.get(id=data["id"]).name == pet_name

    def test_create_pet_with_description(self):
        pet_name = self.faker.name()
        description = self.faker.sentence()
        resp = self.create_single_pet_via_api(pet_name, description)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert data["name"] == pet_name
        assert "id" in data

        assert Pet.objects.filter(id=data["id"]).exists()
        assert Pet.objects.get(id=data["id"]).name == pet_name
        assert Pet.objects.get(id=data["id"]).description == description

    def test_create_multiple_pet(self):

        count = 5

        for _ in range(count):
            pet_name = self.faker.name()
            resp = self.create_single_pet_via_api(pet_name)

            assert resp.status_code == HTTPStatus.CREATED
            data = resp.json()
            assert data["name"] == pet_name
            assert "id" in data

            assert Pet.objects.filter(id=data["id"]).exists()
            assert Pet.objects.get(id=data["id"]).name == pet_name

        assert Pet.objects.count() == count

    def test_create_pet_existing_name(self):
        pet_name = self.faker.name()
        resp = self.create_single_pet_via_api(pet_name)

        assert resp.status_code == HTTPStatus.CREATED

        resp = self.create_single_pet_via_api(pet_name)
        assert resp.status_code == HTTPStatus.BAD_REQUEST
        assert Pet.objects.count() == 1


class TestApiPetsUpdate(GeneratePetsMixin, DirectoriesMixin, TestCase):
    def test_update_pet_name(self):
        self.generate_pet_objects(1)

        instance: Pet = self.pets[0]

        new_name = self.faker.name()

        resp = self.client.patch(
            f"/api/pet/{instance.pk}/",
            content_type="application/json",
            data={"name": new_name},
        )

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert data["name"] == new_name
        assert "id" in data
        created_id = data["id"]
        assert Pet.objects.filter(id=created_id).exists()
        assert Pet.objects.get(id=created_id).name == new_name

    def test_update_pet_description(self):
        self.generate_pet_objects(1)

        instance: Pet = self.pets[0]

        new_desc = self.faker.sentence()

        resp = self.client.patch(
            f"/api/pet/{instance.pk}/",
            content_type="application/json",
            data={"description": new_desc},
        )

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert data["name"] == instance.name
        assert data["description"] == new_desc


class TestApiPetsDelete(GeneratePetsMixin, DirectoriesMixin, TestCase):
    def test_delete_pet(self):
        self.generate_pet_objects(1)

        instance: Pet = self.pets[0]

        resp = self.client.delete(f"/api/pet/{instance.pk}/")

        assert resp.status_code == HTTPStatus.NO_CONTENT
