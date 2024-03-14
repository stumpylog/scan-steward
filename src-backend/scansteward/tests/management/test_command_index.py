import shutil

import pytest
from django.core.management import call_command
from django.test import TestCase

from scansteward.imageops.metadata import read_image_metadata
from scansteward.imageops.metadata import write_image_metadata
from scansteward.imageops.models import RegionStruct
from scansteward.imageops.models import XmpAreaStruct
from scansteward.models import Image
from scansteward.models import Person
from scansteward.models import PersonInImage
from scansteward.models import Pet
from scansteward.models import Tag
from scansteward.tests.mixins import DirectoriesMixin
from scansteward.tests.mixins import SampleDirMixin


class TestIndexCommand(DirectoriesMixin, SampleDirMixin, TestCase):
    def test_call_command_no_files(self):
        call_command("index", str(self.get_new_temporary_dir()))

    def test_call_command_single_file(self):
        tmp_dir = self.get_new_temporary_dir()

        result = shutil.copy(self.SAMPLE_ONE, tmp_dir / self.SAMPLE_ONE.name)

        call_command("index", str(tmp_dir))

        assert Image.objects.count() == 1
        img = Image.objects.first()
        assert img is not None

        # Check the paths were read correctly
        assert img.original == str(result)

        assert img.original_path.exists()
        assert img.original_path.is_file()

        assert img.thumbnail_path.exists()
        assert img.thumbnail_path.is_file()

        assert img.full_size_path.exists()
        assert img.full_size_path.is_file()

        assert img.city == "WASHINGTON"
        assert img.country == "USA"
        assert img.state == "DC"

        # Check the person was read correctly
        assert img.people.count() == 1
        assert Image.objects.count() == 1
        person = img.people.first()
        assert person is not None
        assert person.name == "Barack Obama"
        assert person.description is None

        # Check the region box was read
        face_box = PersonInImage.objects.filter(person=person).first()
        assert face_box is not None
        assert face_box.center_x == pytest.approx(0.317383)
        assert face_box.center_y == pytest.approx(0.303075)
        assert face_box.height == pytest.approx(0.0585652)
        assert face_box.width == pytest.approx(0.0292969)

        assert img.tags.count() == 6
        assert Tag.objects.count() == 6
        # Check tag structure\
        # Pet tag tree
        assert img.tags.filter(name="Pets").exists()
        assert img.tags.filter(name="Dogs").exists()
        assert img.tags.filter(name="Dogs").first().parent == img.tags.filter(name="Pets").first()
        assert img.tags.filter(name="Bo")
        assert img.tags.filter(name="Bo").first().parent == img.tags.filter(name="Dogs").first()
        # Location tag tree
        assert img.tags.filter(name="Locations").exists()
        assert img.tags.filter(name="United States").exists()
        assert (
            img.tags.filter(name="United States").first().parent == img.tags.filter(name="Locations").first()
        )
        assert img.tags.filter(name="Washington DC")
        assert (
            img.tags.filter(name="Washington DC").first().parent
            == img.tags.filter(name="United States").first()
        )

    def test_index_command_file_moved(self):
        tmp_dir = self.get_new_temporary_dir()

        result = shutil.copy(self.SAMPLE_ONE, tmp_dir / self.SAMPLE_ONE.name)

        call_command("index", str(tmp_dir))

        assert Image.objects.count() == 1
        img = Image.objects.first()
        assert img is not None

        assert img.original == str(result)

        new_tmp_dir = self.get_new_temporary_dir()

        new_result = shutil.copy(self.SAMPLE_ONE, new_tmp_dir / self.SAMPLE_ONE.name)

        call_command("index", str(new_tmp_dir))

        assert Image.objects.count() == 1
        img = Image.objects.first()
        assert img is not None

        assert img.original == str(new_result)

    def test_index_command_multiple_files(self):
        tmp_dir = self.get_new_temporary_dir()

        for file in self.ALL_SAMPLE_IMAGES:
            shutil.copy(file, tmp_dir / file.name)

        call_command("index", str(tmp_dir))

        # 4 images expected
        assert Image.objects.count() == len(self.ALL_SAMPLE_IMAGES)
        # No duplicated people
        assert Person.objects.count() == 4
        assert Person.objects.filter(name="Barack Obama").exists()
        assert Person.objects.filter(name="Joseph R Biden").exists()
        assert Person.objects.filter(name="Hillary Clinton").exists()
        assert Person.objects.filter(name="Denis McDonough").exists()
        # Present in 4 images
        assert Person.objects.filter(name="Barack Obama").first().images.count() == 4
        # Only in 1 image
        assert Person.objects.filter(name="Hillary Clinton").first().images.count() == 1

    def test_index_command_with_region_description(self):
        tmp_dir = self.get_new_temporary_dir()

        result = shutil.copy(self.SAMPLE_ONE, tmp_dir / self.SAMPLE_ONE.name)

        metdata = read_image_metadata(result)

        metdata.RegionInfo.RegionList[0].Description = "This is a description of a region"

        write_image_metadata(metdata)

        call_command("index", str(tmp_dir))

        assert Image.objects.count() == 1
        img = Image.objects.first()
        assert img is not None

        # Check the person was read correctly
        assert img.people.count() == 1
        assert Image.objects.count() == 1
        person = img.people.first()
        assert person is not None
        assert person.name == "Barack Obama"
        assert person.description == "This is a description of a region"

    def test_index_command_with_pets(self):
        tmp_dir = self.get_new_temporary_dir()

        result = shutil.copy(self.SAMPLE_ONE, tmp_dir / self.SAMPLE_ONE.name)

        metdata = read_image_metadata(result)

        metdata.RegionInfo.RegionList.append(
            RegionStruct(
                Area=XmpAreaStruct(
                    H=0.0585652,
                    W=0.0292969,
                    X=0.317383,
                    Y=0.303075,
                    Unit="normalized",
                    D=None,
                ),
                Name="Some Pet",
                Type="Pet",
                Description="This was a pet",
            ),
        )

        write_image_metadata(metdata)

        call_command("index", str(tmp_dir))

        assert Pet.objects.count() == 1
        instance = Pet.objects.filter(name="Some Pet").first()
        assert instance is not None
        assert instance.name == "Some Pet"
        assert instance.description == "This was a pet"
