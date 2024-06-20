import zipfile
from http import HTTPStatus

import pytest
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import Client

from scansteward.models import Album
from scansteward.models import Image
from scansteward.tests.api.utils import FakerMixin
from scansteward.tests.api.utils import GenerateImagesMixin
from scansteward.tests.mixins import DirectoriesMixin
from scansteward.tests.mixins import IndexedEnvironmentMixin


def create_single_album(client: Client, name: str, description: str | None = None) -> HttpResponse:
    data = {"name": name}
    if description is not None:
        data.update({"description": description})
    return client.post(
        "/api/album/",
        content_type="application/json",
        data=data,
    )


class TestApiAlbumRead(FakerMixin, DirectoriesMixin, TestCase):
    def test_read_no_albums(self):
        """
        GIVEN:
            - No albums in the database
        WHEN:
            - Requesting to read all albums
        THEN:
            - Return an empty list of albums
        """
        resp = self.client.get(
            "/api/album/",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == 0
        assert len(data["items"]) == 0

    def test_read_albums(self):
        """
        GIVEN:
            - Albums in the database
        WHEN:
            - Requesting to read all albums
        THEN:
            - Return a list of albums
        """
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


class TestApiAlbumCreate(FakerMixin, DirectoriesMixin, TestCase):
    def test_create_album(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert {"id": 1, "name": album_name, "description": None} == data

        assert Album.objects.filter(id=data["id"]).exists()
        assert Album.objects.get(id=data["id"]).name == album_name
        assert Album.objects.get(id=data["id"]).images.count() == 0

    def test_create_album_with_description(self):
        album_name = self.faker.unique.name()
        desc = self.faker.unique.sentence()
        resp = create_single_album(self.client, album_name, desc)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert {"id": 1, "name": album_name, "description": desc} == data

        assert Album.objects.filter(id=data["id"]).exists()
        assert Album.objects.get(id=data["id"]).name == album_name
        assert Album.objects.get(id=data["id"]).description == desc
        assert Album.objects.get(id=data["id"]).images.count() == 0


class TestApiAlbumUpdate(FakerMixin, DirectoriesMixin, TestCase):
    def test_update_album(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert {"id": 1, "name": album_name, "description": None} == data
        album_id = data["id"]

        assert Album.objects.filter(id=album_id).exists()
        assert Album.objects.get(id=album_id).name == album_name
        assert Album.objects.get(id=album_id).images.count() == 0

        new_name = "A New Name"

        assert album_name != new_name

        resp = self.client.patch(
            f"/api/album/{album_id}/",
            content_type="application/json",
            data={"name": new_name},
        )

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert {"id": album_id, "name": new_name, "description": None} == data
        assert Album.objects.filter(id=album_id).exists()
        assert Album.objects.get(id=album_id).name == new_name
        assert Album.objects.get(id=album_id).images.count() == 0

    def test_add_album_description(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert {"id": 1, "name": album_name, "description": None} == data
        album_id = data["id"]
        assert Album.objects.get(id=album_id).name == album_name
        assert Album.objects.get(id=album_id).description is None

        desc = "This is a description"

        resp = self.client.patch(
            f"/api/album/{album_id}/",
            content_type="application/json",
            data={"description": desc},
        )

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert {"id": album_id, "name": album_name, "description": desc} == data
        assert Album.objects.get(id=album_id).name == album_name
        assert Album.objects.get(id=album_id).description == desc


class TestApiAlbumDelete(FakerMixin, DirectoriesMixin, TestCase):
    def test_delete_album(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert {"id": 1, "name": album_name, "description": None} == data
        album_id = data["id"]

        resp = self.client.delete(f"/api/album/{album_id}/")

        assert resp.status_code == HTTPStatus.NO_CONTENT

    def test_delete_does_not_exist(self):
        resp = self.client.delete("/api/album/1/")

        assert resp.status_code == HTTPStatus.NOT_FOUND


class TestApiAlbumImages(GenerateImagesMixin, DirectoriesMixin, TestCase):
    def test_add_single_image(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        self.generate_image_objects(1)
        img = self.images[0]

        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [img.pk]},
        )

        assert resp.status_code == HTTPStatus.OK
        assert {"name": album_name, "description": None, "id": album_id, "image_ids": [img.pk]} == resp.json()

        resp = self.client.get(f"/api/album/{album_id}/")

        assert resp.status_code == HTTPStatus.OK
        assert {"name": album_name, "description": None, "id": album_id, "image_ids": [img.pk]} == resp.json()

    def test_add_multiple_images(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        self.generate_image_objects(2)

        img_one = self.images[0]
        img_two = self.images[1]

        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [img_one.pk, img_two.pk]},
        )

        assert resp.status_code == HTTPStatus.OK
        assert {
            "name": album_name,
            "description": None,
            "id": album_id,
            "image_ids": [img_one.pk, img_two.pk],
        } == resp.json()

        album = Album.objects.get(pk=album_id)

        assert album.images.count() == 2

    def test_remove_image(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        count = 5
        self.generate_image_objects(count)
        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [img.pk for img in self.images]},
        )
        assert resp.status_code == HTTPStatus.OK

        test_img = self.images[0]
        resp = self.client.patch(
            f"/api/album/{album_id}/remove/",
            content_type="application/json",
            data={"image_ids": [test_img.pk]},
        )
        assert resp.status_code == HTTPStatus.OK
        assert {
            "name": album_name,
            "description": None,
            "id": album_id,
            "image_ids": [x.pk for x in self.images[1:]],
        } == resp.json()

    def test_remove_image_not_in_album(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        count = 5
        self.generate_image_objects(count)
        dont_add = 4
        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [img.pk for img in self.images if img.pk != dont_add]},
        )
        assert resp.status_code == HTTPStatus.OK

        not_added_image = Image.objects.get(pk=dont_add)

        with self.assertLogs() as cm:
            resp = self.client.patch(
                f"/api/album/{album_id}/remove/",
                content_type="application/json",
                data={"image_ids": [not_added_image.pk]},
            )
            assert len(cm.records) == 1
            record = cm.records[0]
            assert record.message == f"Image {not_added_image.pk} not in album {album_id}"
        assert resp.status_code == HTTPStatus.OK

        resp = self.client.get(f"/api/album/{album_id}/")
        assert resp.status_code == HTTPStatus.OK
        assert {
            "name": album_name,
            "description": None,
            "id": album_id,
            "image_ids": [x.pk for x in self.images if x.pk != dont_add],
        } == resp.json()

    def test_remove_last_album_image(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        count = 5
        self.generate_image_objects(count)

        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [img.pk for img in self.images]},
        )
        assert resp.status_code == HTTPStatus.OK

        test_img = self.images[-1]
        resp = self.client.patch(
            f"/api/album/{album_id}/remove/",
            content_type="application/json",
            data={"image_ids": [test_img.pk]},
        )
        assert resp.status_code == HTTPStatus.OK
        assert {
            "name": album_name,
            "description": None,
            "id": album_id,
            "image_ids": [x.pk for x in self.images[0:-1]],
        } == resp.json()

    def test_add_remove_no_items(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        count = 5
        self.generate_image_objects(count)

        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [img.pk for img in self.images]},
        )
        assert resp.status_code == HTTPStatus.OK

        resp = self.client.patch(
            f"/api/album/{album_id}/remove/",
            content_type="application/json",
            data={"image_ids": []},
        )

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": []},
        )

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


class TestApiAlbumSorting(GenerateImagesMixin, DirectoriesMixin, TestCase):
    def test_update_sorting_reversed(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        count = 5
        self.generate_image_objects(count)
        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [img.pk for img in self.images]},
        )
        assert resp.status_code == HTTPStatus.OK

        resp = self.client.get(f"/api/album/{album_id}/")
        assert resp.status_code == HTTPStatus.OK
        assert (
            resp.json()
            == {
                "name": album_name,
                "description": None,
                "id": album_id,
                "image_ids": [x.pk for x in self.images],
            }
            == resp.json()
        )

        resp = self.client.patch(
            f"/api/album/{album_id}/sort/",
            content_type="application/json",
            data={"sorting": [x.pk for x in reversed(self.images)]},
        )

        assert resp.status_code == HTTPStatus.OK
        assert (
            resp.json()
            == {
                "name": album_name,
                "description": None,
                "id": album_id,
                "image_ids": [x.pk for x in reversed(self.images)],
            }
            == resp.json()
        )

    def test_custom_sorting(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        count = 5
        self.generate_image_objects(count)
        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [x.pk for x in self.images]},
        )
        assert resp.status_code == HTTPStatus.OK

        resp = self.client.patch(
            f"/api/album/{album_id}/sort/",
            content_type="application/json",
            data={
                "sorting": [
                    self.images[1].pk,
                    self.images[0].pk,
                    self.images[2].pk,
                    self.images[4].pk,
                    self.images[3].pk,
                ],
            },
        )

        assert resp.status_code == HTTPStatus.OK
        assert (
            resp.json()
            == {
                "name": album_name,
                "description": None,
                "id": album_id,
                "image_ids": [
                    self.images[1].pk,
                    self.images[0].pk,
                    self.images[2].pk,
                    self.images[4].pk,
                    self.images[3].pk,
                ],
            }
            == resp.json()
        )

    def test_sorting_invalid_length(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        count = 5
        self.generate_image_objects(count)
        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [x.pk for x in self.images]},
        )
        assert resp.status_code == HTTPStatus.OK

        resp = self.client.patch(
            f"/api/album/{album_id}/sort/",
            content_type="application/json",
            data={
                "sorting": [
                    self.images[1].pk,
                    self.images[3].pk,
                ],
            },
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST

    def test_update_sorting_with_no_sorting_defined(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        count = 5
        self.generate_image_objects(count)
        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [x.pk for x in self.images]},
        )
        assert resp.status_code == HTTPStatus.OK

        resp = self.client.patch(
            f"/api/album/{album_id}/sort/",
            content_type="application/json",
            data={
                "sorting": [],
            },
        )

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


class TestApiAlbumDownload(IndexedEnvironmentMixin, FakerMixin, TestCase):
    def download_test_common(self, *, use_original_download=False):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        resp = self.client.patch(
            f"/api/album/{album_id}/add/",
            content_type="application/json",
            data={"image_ids": [image.pk for image in Image.objects.all()]},
        )
        assert resp.status_code == HTTPStatus.OK

        # Download album
        if not use_original_download:
            resp = self.client.get(f"/api/album/{album_id}/download/")
        else:
            resp = self.client.get(f"/api/album/{album_id}/download/?zip_originals=True")
        assert resp.status_code == HTTPStatus.OK

        zipped_album = self.get_new_temporary_dir() / "test.zip"
        zipped_album.write_bytes(b"".join(resp.streaming_content))

        with zipfile.ZipFile(zipped_album) as downloaded_zip:
            info = downloaded_zip.infolist()
            assert len(info) == 4
            for index, image in enumerate(
                Album.objects.get(id=album_id).images.order_by("imageinalbum__sort_order").all(),
            ):
                if not use_original_download:
                    arcname = f"{index + 1:010}{image.full_size_path.suffix}"
                else:
                    arcname = f"{index + 1:010}{image.original_path.suffix}"
                try:
                    downloaded_zip.getinfo(arcname)
                except KeyError:
                    pytest.fail(f"{arcname} not present in zipfile")

    def test_album_download_full_size(self):
        self.download_test_common(use_original_download=False)

    def test_album_download_original(self):
        self.download_test_common(use_original_download=True)

    def test_album_no_images(self):
        album_name = self.faker.unique.name()
        resp = create_single_album(self.client, album_name)

        assert resp.status_code == HTTPStatus.CREATED
        album_id = resp.json()["id"]

        resp = self.client.get(f"/api/album/{album_id}/download/")

        assert resp.status_code == HTTPStatus.BAD_REQUEST
