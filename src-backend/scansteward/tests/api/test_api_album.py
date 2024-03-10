from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase

from scansteward.models import Album
from scansteward.tests.api.utils import FakerTestCase


class TestApiAlbumRead(FakerTestCase, TestCase):
    def test_read_no_albums(self):
        Album.objects.all().delete()
        resp = self.client.get(
            "/api/album/",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == 0
        assert len(data["items"]) == 0

    def test_read_albums(self):
        count = 11
        names = []
        for _ in range(count):
            name = self.faker.unique.name()
            Album.objects.create(name=name)
            names.append(name)
        resp = self.client.get(
            "/api/album/",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == count
        assert len(data["items"]) == count
        assert names == [x["name"] for x in data["items"]]

    def test_get_single_album(self):
        instance = Album.objects.create(name=self.faker.unique.name())

        resp = self.client.get(f"/api/album/{instance.pk}/")

        assert resp.status_code == HTTPStatus.OK
        assert resp.json()["name"] == instance.name


class TestApiAlbumCreate(FakerTestCase, TestCase):

    def create_single_album(self, name: str, description: str | None = None) -> HttpResponse:
        data = {"name": name}
        if description is not None:
            data.update({"description": description})
        return self.client.post(
            "/api/album/",
            content_type="application/json",
            data=data,
        )

    def test_create_album(self):
        album_name = self.faker.unique.name()
        resp = self.create_single_album(album_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert data["name"] == album_name
        assert "id" in data

        assert Album.objects.filter(id=data["id"]).exists()
        assert Album.objects.get(id=data["id"]).name == album_name
        assert Album.objects.get(id=data["id"]).images.count() == 0

    def test_create_album_with_description(self):
        album_name = self.faker.unique.name()
        desc = self.faker.unique.sentence()
        resp = self.create_single_album(album_name, desc)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert data["name"] == album_name
        assert "id" in data

        assert Album.objects.filter(id=data["id"]).exists()
        assert Album.objects.get(id=data["id"]).name == album_name
        assert Album.objects.get(id=data["id"]).description == desc
        assert Album.objects.get(id=data["id"]).images.count() == 0


class TestApiAlbumUpdate(FakerTestCase, TestCase):
    def create_single_album(self, name: str, description: str | None = None) -> HttpResponse:
        data = {"name": name}
        if description is not None:
            data.update({"description": description})
        return self.client.post(
            "/api/album/",
            content_type="application/json",
            data=data,
        )

    def test_update_album(self):
        album_name = self.faker.unique.name()
        resp = self.create_single_album(album_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert data["name"] == album_name
        assert "id" in data
        id = data["id"]

        assert Album.objects.filter(id=id).exists()
        assert Album.objects.get(id=id).name == album_name
        assert Album.objects.get(id=id).images.count() == 0

        new_name = "A New Name"

        assert album_name != new_name

        resp = self.client.patch(
            f"/api/album/{id}/",
            content_type="application/json",
            data={"name": new_name},
        )

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert data["name"] == new_name
        assert Album.objects.get(id=id).name == new_name

    def test_add_album_description(self):
        album_name = self.faker.unique.name()
        resp = self.create_single_album(album_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert "id" in data
        id = data["id"]
        assert Album.objects.get(id=id).name == album_name
        assert Album.objects.get(id=id).description is None

        desc = "This is a description"

        resp = self.client.patch(
            f"/api/album/{id}/",
            content_type="application/json",
            data={"description": desc},
        )

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert "id" in data
        id = data["id"]
        assert Album.objects.get(id=id).name == album_name
        assert Album.objects.get(id=id).description == desc


class TestApiAlbumDelete(TestCase):
    pass


class TestApiAlbumImages(TestCase):
    pass


class TestApiAlbumSorting(TestCase):
    pass
