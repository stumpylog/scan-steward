import random
import shutil
from http import HTTPStatus

from django.core.management import call_command
from django.test import TestCase

from scansteward.models import Image
from scansteward.models import Person
from scansteward.models import PersonInImage
from scansteward.models import Pet
from scansteward.models import PetInImage
from scansteward.tests.mixins import DirectoriesMixin
from scansteward.tests.mixins import FileSystemAssertsMixin
from scansteward.tests.mixins import SampleDirMixin


class TestImageFileReads(DirectoriesMixin, SampleDirMixin, FileSystemAssertsMixin, TestCase):
    def util_index_one_file(self):
        tmp_dir = self.get_new_temporary_dir()

        self.temp_sample_one = shutil.copy(self.SAMPLE_ONE, tmp_dir / self.SAMPLE_ONE.name)

        call_command("index", str(tmp_dir))

    def test_image_generated_files_match(self):
        self.util_index_one_file()

        img = Image.objects.first()
        assert img is not None

        # Thumbnail
        assert img.thumbnail_path.exists()
        assert img.thumbnail_path.is_file()

        resp = self.client.get(f"/api/image/{img.pk}/thumbnail/")

        assert resp.status_code == HTTPStatus.OK
        assert resp["ETag"] == f'"{img.thumbnail_checksum}"'
        assert resp["Last-Modified"] == img.modified.strftime("%a, %d %b %Y %H:%M:%S GMT")

        thumbnail_data = b"".join(resp.streaming_content)

        self.assertFileContents(img.thumbnail_path, thumbnail_data)

        # Fullsize, WebP
        assert img.full_size_path.exists()
        assert img.full_size_path.is_file()

        resp = self.client.get(f"/api/image/{img.pk}/full/")

        assert resp.status_code == HTTPStatus.OK
        assert resp["ETag"] == f'"{img.full_size_checksum}"'
        assert resp["Last-Modified"] == img.modified.strftime("%a, %d %b %Y %H:%M:%S GMT")

        full_size_data = b"".join(resp.streaming_content)

        self.assertFileContents(img.full_size_path, full_size_data)

        # Original
        assert img.original_path.exists()
        assert img.original_path.is_file()
        assert img.original_path == self.temp_sample_one

        resp = self.client.get(f"/api/image/{img.pk}/original/")

        assert resp.status_code == HTTPStatus.OK
        assert resp["Content-Type"] == "image/jpeg"
        assert resp["ETag"] == f'"{img.original_checksum}"'
        assert resp["Content-Length"] == str(img.file_size)
        assert resp["Last-Modified"] == img.modified.strftime("%a, %d %b %Y %H:%M:%S GMT")

        original_data = b"".join(resp.streaming_content)

        self.assertFileContents(img.original_path, original_data)


class TestImageReadApi(DirectoriesMixin, SampleDirMixin, TestCase):
    def util_index_one_file(self):
        tmp_dir = self.get_new_temporary_dir()

        self.temp_sample_one = shutil.copy(self.SAMPLE_ONE, tmp_dir / self.SAMPLE_ONE.name)

        # TODO: This is fixed data and could be done purely in the database instead of indexing each time

        call_command("index", str(tmp_dir))

    def test_get_image_faces(self):
        """
        Test
        """
        self.util_index_one_file()

        img = Image.objects.first()
        assert img is not None

        resp = self.client.get(f"/api/image/{img.pk}/faces/")
        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert [
            {
                "box": {
                    "center_x": 0.317383,
                    "center_y": 0.303075,
                    "height": 0.0585652,
                    "width": 0.0292969,
                },
                "person_id": 1,
            },
        ] == data

    def test_get_image_pets(self):
        # TODO: Digikam does not support pet boxes as of yet.  Need to create the manually with exiftool

        self.util_index_one_file()

        img = Image.objects.first()
        assert img is not None

        resp = self.client.get(f"/api/image/{img.pk}/pets/")
        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert [
            {
                "pet_id": 1,
                "box": {
                    "center_x": 0.616699,
                    "center_y": 0.768668,
                    "height": 0.284041,
                    "width": 0.202148,
                },
            },
        ] == data

    def test_get_image_metadata(self):
        self.util_index_one_file()

        img = Image.objects.first()
        assert img is not None

        resp = self.client.get(f"/api/image/{img.pk}/metadata/")
        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert {
            "album_ids": None,
            "date_id": 1,
            "description": (
                "President Barack Obama throws a ball for Bo, the family dog, "
                "in the Rose Garden of the White House, Sept. 9, 2010.  "
                "(Official White House Photo by Pete Souza)"
            ),
            "location_id": 1,
            "orientation": 1,
            "tag_ids": [3],
        } == data


class TestImageUpdateApi(DirectoriesMixin, SampleDirMixin, TestCase):
    def util_create_image_in_database(self) -> Image:
        image = Image.objects.create(
            file_size=random.randint(1, 1_000_000),  # noqa: S311
            original_checksum="abcd",
            thumbnail_checksum="efgh",
            full_size_checksum="ijkl",
            phash="mnop",
            original=self.SAMPLE_DIR / "test.jpg",
            description="test description",
        )

        person = Person.objects.create(name="Test Person")
        _ = PersonInImage.objects.create(
            person=person,
            image=image,
            center_x=0.1,
            center_y=0.2,
            height=0.3,
            width=0.4,
        )
        pet = Pet.objects.create(name="Test Pet")
        PetInImage.objects.create(
            pet=pet,
            image=image,
            center_x=0.5,
            center_y=0.6,
            height=0.7,
            width=0.8,
        )

        image.refresh_from_db()
        return image

    def test_update_face_bounding_box(self):
        pass

    def test_update_pet_bounding_box(self):
        pass

    def test_update_image_metadata(self):
        pass


class TestImageCreateApi(DirectoriesMixin, SampleDirMixin, TestCase):
    def test_add_faces_to_image(self):
        pass

    def test_add_pet_box_to_image(self):
        pass


class TestImageDeleteApi(DirectoriesMixin, SampleDirMixin, TestCase):
    def test_delete_face_from_image(self):
        pass

    def test_delete_pet_from_image(self):
        pass
