import shutil
from http import HTTPStatus

from django.core.management import call_command
from django.test import TestCase

from scansteward.imageops.models import RotationEnum
from scansteward.models import Image
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
        thumbnail_data = b"".join(resp.streaming_content)

        self.assertFileContents(img.thumbnail_path, thumbnail_data)

        # Fullsize, WebP
        assert img.full_size_path.exists()
        assert img.full_size_path.is_file()

        resp = self.client.get(f"/api/image/{img.pk}/full/")

        assert resp.status_code == HTTPStatus.OK
        full_size_data = b"".join(resp.streaming_content)

        self.assertFileContents(img.full_size_path, full_size_data)

        # Original
        assert img.original_path.exists()
        assert img.original_path.is_file()
        assert img.original_path == self.temp_sample_one

        resp = self.client.get(f"/api/image/{img.pk}/original/")

        assert resp.status_code == HTTPStatus.OK
        original_data = b"".join(resp.streaming_content)

        self.assertFileContents(img.original_path, original_data)


class TestImageDetails(DirectoriesMixin, SampleDirMixin, TestCase):
    def util_index_one_file(self):
        tmp_dir = self.get_new_temporary_dir()

        self.temp_sample_one = shutil.copy(self.SAMPLE_ONE, tmp_dir / self.SAMPLE_ONE.name)

        call_command("index", str(tmp_dir))

    def test_get_image_details(self):
        self.util_index_one_file()

        img = Image.objects.first()
        assert img is not None

        resp = self.client.get(f"/api/image/{img.pk}/")
        assert resp.status_code == HTTPStatus.OK
        assert {
            "albums": [],
            "orientation": RotationEnum.HORIZONTAL.value,
            "description": (
                "President Barack Obama throws a ball for Bo, the family dog, "
                "in the Rose Garden of the White House, Sept. 9, 2010.  "
                "(Official White House Photo by Pete Souza)"
            ),
            "face_boxes": [
                {
                    "box": {
                        "center_x": 0.317383,
                        "center_y": 0.303075,
                        "height": 0.0585652,
                        "width": 0.0292969,
                    },
                    "person": {"description": None, "id": 1, "name": "Barack Obama"},
                },
            ],
            "pet_boxes": [],
            "tags": [
                {"applied": False, "description": None, "id": 1, "name": "Pets", "parent_id": None},
                {"applied": False, "description": None, "id": 2, "name": "Dogs", "parent_id": 1},
                {"applied": False, "description": None, "id": 3, "name": "Bo", "parent_id": 2},
                {"applied": False, "description": None, "id": 4, "name": "Locations", "parent_id": None},
                {"applied": False, "description": None, "id": 5, "name": "United States", "parent_id": 4},
                {"applied": False, "description": None, "id": 6, "name": "Washington DC", "parent_id": 5},
            ],
            "location": {
                "city": "WASHINGTON",
                "country_code": "US",
                "sub_location": None,
                "subdivision_code": "US-DC",
            },
        } == resp.json()
