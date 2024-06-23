import datetime
import random
from http import HTTPStatus
from pathlib import Path

import pytest
from django.test.client import Client

from scansteward.imageops.models import RotationEnum
from scansteward.models import Image
from scansteward.models import Person
from scansteward.models import PersonInImage
from scansteward.models import Pet
from scansteward.models import PetInImage
from scansteward.models import RoughDate
from scansteward.models import RoughLocation
from scansteward.tests.mixins import DirectoriesMixin
from scansteward.tests.mixins import FileSystemAssertsMixin

# from scansteward.tests.mixins import SampleDirMixin


def util_create_image_in_database(sample_dir: Path) -> tuple[Image, Person, Pet]:
    image = Image.objects.create(
        file_size=random.randint(1, 1_000_000),  # noqa: S311
        original_checksum="abcd",
        thumbnail_checksum="efgh",
        full_size_checksum="ijkl",
        phash="mnop",
        original=sample_dir / "test.jpg",
        description="test description",
        height=random.randint(100, 200),  # noqa: S311
        width=random.randint(100, 200),  # noqa: S311
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
    return image, person, pet


@pytest.mark.usefixtures("sample_image_environment")
@pytest.mark.django_db()
class TestImageFileReads(FileSystemAssertsMixin):
    def test_image_generated_files_match(self, client: Client):
        img = Image.objects.first()
        assert img is not None

        # Thumbnail
        assert img.thumbnail_path.exists()
        assert img.thumbnail_path.is_file()

        resp = client.get(f"/api/image/{img.pk}/thumbnail/")

        assert resp.status_code == HTTPStatus.OK
        assert resp["ETag"] == f'"{img.thumbnail_checksum}"'
        assert resp["Last-Modified"] == img.modified.strftime("%a, %d %b %Y %H:%M:%S GMT")

        thumbnail_data = b"".join(resp.streaming_content)

        self.assertFileContents(img.thumbnail_path, thumbnail_data)

        # Fullsize, WebP
        assert img.full_size_path.exists()
        assert img.full_size_path.is_file()

        resp = client.get(f"/api/image/{img.pk}/full/")

        assert resp.status_code == HTTPStatus.OK
        assert resp["ETag"] == f'"{img.full_size_checksum}"'
        assert resp["Last-Modified"] == img.modified.strftime("%a, %d %b %Y %H:%M:%S GMT")

        full_size_data = b"".join(resp.streaming_content)

        self.assertFileContents(img.full_size_path, full_size_data)

        # Original
        assert img.original_path.exists()
        assert img.original_path.is_file()

        resp = client.get(f"/api/image/{img.pk}/original/")

        assert resp.status_code == HTTPStatus.OK
        assert resp["Content-Type"] == "image/jpeg"
        assert resp["ETag"] == f'"{img.original_checksum}"'
        assert resp["Content-Length"] == str(img.file_size)
        assert resp["Last-Modified"] == img.modified.strftime("%a, %d %b %Y %H:%M:%S GMT")

        original_data = b"".join(resp.streaming_content)

        self.assertFileContents(img.original_path, original_data)


@pytest.mark.usefixtures("sample_image_environment")
@pytest.mark.django_db()
class TestImageReadApi:
    def test_get_image_faces(self, client: Client):
        img = Image.objects.last()
        assert img is not None

        resp = client.get(f"/api/image/{img.pk}/faces/")
        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert [
            {
                "box": {
                    "center_x": 0.466361,
                    "center_y": 0.186927,
                    "height": 0.0940367,
                    "width": 0.0428135,
                },
                "person_id": 1,
            },
        ] == data

    def test_get_image_pets(self, client: Client):
        img = Image.objects.first()
        assert img is not None

        resp = client.get(f"/api/image/{img.pk}/pets/")
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

    def test_get_image_metadata(self, client: Client):
        img = Image.objects.first()
        assert img is not None

        resp = client.get(f"/api/image/{img.pk}/metadata/")
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
            "orientation": RotationEnum.HORIZONTAL,
            "tag_ids": [3],
        } == data


@pytest.mark.usefixtures("sample_image_environment")
@pytest.mark.django_db()
class TestImageUpdateApi:
    def test_update_face_bounding_box(self, client: Client):
        image = Image.objects.last()
        assert image is not None
        person = image.people.first()
        assert person is not None

        resp = client.patch(
            f"/api/image/{image.pk}/faces/",
            content_type="application/json",
            data=[
                {
                    "person_id": person.pk,
                    "box": {"center_x": 0.5, "center_y": 0.3, "height": 0.1, "width": 0.9},
                },
            ],
        )
        assert resp.status_code == HTTPStatus.OK

        new_box = PersonInImage.objects.get(image=image, person=person)
        assert new_box is not None
        assert new_box.center_x == 0.5
        assert new_box.center_y == 0.3
        assert new_box.height == 0.1
        assert new_box.width == 0.9

    def test_update_pet_bounding_box(self, client: Client):
        image = Image.objects.first()
        assert image is not None
        pet = image.pets.first()
        assert pet is not None

        resp = client.patch(
            f"/api/image/{image.pk}/pets/",
            content_type="application/json",
            data=[
                {
                    "pet_id": pet.pk,
                    "box": {"center_x": 0.5, "center_y": 0.3, "height": 0.1, "width": 0.9},
                },
            ],
        )
        assert resp.status_code == HTTPStatus.OK

        new_box = PetInImage.objects.get(image=image, pet=pet)
        assert new_box is not None
        assert new_box.center_x == 0.5
        assert new_box.center_y == 0.3
        assert new_box.height == 0.1
        assert new_box.width == 0.9

    def test_update_image_metadata(self, client: Client, date_today_utc: datetime.date):
        image = Image.objects.last()
        assert image is not None

        new_loc = RoughLocation.objects.create(country_code="US")
        new_date = RoughDate.objects.create(date=date_today_utc)

        resp = client.get(f"/api/image/{image.pk}/metadata/")
        assert resp.status_code == HTTPStatus.OK

        existing = resp.json()
        existing["orientation"] = RotationEnum.MIRROR_HORIZONTAL
        existing["description"] = "New Desc"
        existing["location_id"] = new_loc.pk
        existing["date_id"] = new_date.pk

        resp = client.patch(f"/api/image/{image.pk}/metadata/", content_type="application/json", data=existing)
        assert resp.status_code == HTTPStatus.OK


@pytest.mark.usefixtures("sample_image_environment")
@pytest.mark.django_db()
class TestImageCreateApi(DirectoriesMixin):
    def test_add_faces_to_image(self):
        pass

    def test_add_pet_box_to_image(self):
        pass


@pytest.mark.usefixtures("sample_image_environment")
@pytest.mark.django_db()
class TestImageDeleteApi(DirectoriesMixin):
    def test_delete_face_from_image(self, client: Client):
        image = Image.objects.first()
        assert image is not None
        person = image.people.first()
        assert person is not None

        initial_people_count = Person.objects.count()
        initial_pet_count = Pet.objects.count()
        initial_box_count = PersonInImage.objects.count()
        initial_people_in_img_count = image.people.count()
        initial_pet_in_img_count = image.pets.count()

        resp = client.delete(
            f"/api/image/{image.pk}/faces/",
            content_type="application/json",
            data={"people_ids": [person.pk]},
        )
        assert resp.status_code == HTTPStatus.OK

        image.refresh_from_db()

        assert image.people.count() == (initial_people_in_img_count - 1)
        assert image.pets.count() == initial_pet_in_img_count
        assert PersonInImage.objects.count() == (initial_box_count - 1)
        assert Pet.objects.count() == initial_pet_count
        assert Person.objects.count() == initial_people_count

    def test_delete_face_from_image_not_in_image(self, client: Client):
        image = Image.objects.last()
        assert image is not None
        person = image.people.first()
        assert person is not None

        initial_people_count = Person.objects.count()
        initial_pet_count = Pet.objects.count()
        initial_pet_box_count = PetInImage.objects.count()
        initial_person_box_count = PersonInImage.objects.count()
        initial_people_in_img_count = image.people.count()
        initial_pet_in_img_count = image.pets.count()

        resp = client.delete(
            f"/api/image/{image.pk}/faces/",
            content_type="application/json",
            data={"people_ids": [person.pk + 5]},
        )
        assert resp.status_code == HTTPStatus.OK

        image.refresh_from_db()

        assert image.people.count() == initial_people_in_img_count
        assert image.pets.count() == initial_pet_in_img_count
        assert PersonInImage.objects.count() == initial_person_box_count
        assert PetInImage.objects.count() == initial_pet_box_count
        assert Pet.objects.count() == initial_pet_count
        assert Person.objects.count() == initial_people_count

    def test_delete_pet_from_image(self, client: Client):
        image = Image.objects.first()
        assert image is not None
        pet = image.pets.first()
        assert pet is not None

        initial_people_count = Person.objects.count()
        initial_pet_count = Pet.objects.count()
        initial_pet_box_count = PetInImage.objects.count()
        initial_person_box_count = PersonInImage.objects.count()
        initial_people_in_img_count = image.people.count()
        initial_pet_in_img_count = image.pets.count()

        resp = client.delete(
            f"/api/image/{image.pk}/pets/",
            content_type="application/json",
            data={"pet_ids": [pet.pk]},
        )
        assert resp.status_code == HTTPStatus.OK

        image.refresh_from_db()

        assert image.people.count() == initial_people_in_img_count
        assert image.pets.count() == (initial_pet_in_img_count - 1)
        assert PersonInImage.objects.count() == initial_person_box_count
        assert PetInImage.objects.count() == (initial_pet_box_count - 1)
        assert Pet.objects.count() == initial_pet_count
        assert Person.objects.count() == initial_people_count

    def test_delete_pet_from_image_not_in(self, client: Client):
        image = Image.objects.first()
        assert image is not None
        pet = image.pets.first()
        assert pet is not None

        initial_people_count = Person.objects.count()
        initial_pet_count = Pet.objects.count()
        initial_pet_box_count = PetInImage.objects.count()
        initial_person_box_count = PersonInImage.objects.count()
        initial_people_in_img_count = image.people.count()
        initial_pet_in_img_count = image.pets.count()

        resp = client.delete(
            f"/api/image/{image.pk}/pets/",
            content_type="application/json",
            data={"pet_ids": [pet.pk + 1]},
        )
        assert resp.status_code == HTTPStatus.OK

        image.refresh_from_db()

        assert image.people.count() == initial_people_in_img_count
        assert image.pets.count() == initial_pet_in_img_count
        assert PersonInImage.objects.count() == initial_person_box_count
        assert PetInImage.objects.count() == initial_pet_box_count
        assert Pet.objects.count() == initial_pet_count
        assert Person.objects.count() == initial_people_count
