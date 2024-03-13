import shutil
from pathlib import Path

import pytest

from scansteward.imageops.errors import ImagePathNotFileError
from scansteward.imageops.errors import NoImageMetadataError
from scansteward.imageops.errors import NoImagePathsError
from scansteward.imageops.metadata import bulk_read_image_metadata
from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.metadata import clear_existing_metadata
from scansteward.imageops.metadata import read_image_metadata
from scansteward.imageops.metadata import write_image_metadata
from scansteward.imageops.models import KeywordInfoModel
from scansteward.imageops.models import KeywordStruct
from scansteward.imageops.models import XmpAreaStruct
from scansteward.tests.mixins import SampleDirMixin
from scansteward.tests.mixins import SampleMetadataMixin


class TestReadImageMetadata(
    SampleMetadataMixin,
    SampleDirMixin,
):

    def test_read_single_image_metadata(self):

        metadata = read_image_metadata(self.SAMPLE_ONE)

        self.verify_sample_one_metadata(self.SAMPLE_ONE, metadata)

    def test_bulk_read_image_faces(self):
        metadata = bulk_read_image_metadata(
            [self.SAMPLE_ONE, self.SAMPLE_TWO],
        )

        assert len(metadata) == 2

        self.verify_sample_one_metadata(self.SAMPLE_ONE, metadata[0])
        self.verify_sample_two_metadata(self.SAMPLE_TWO, metadata[1])

    def test_change_single_image_metadata(self, temporary_directory: Path):

        new_sample_one = Path(shutil.copy(self.SAMPLE_ONE, temporary_directory / self.SAMPLE_ONE.name))

        # Change something
        new_metadata = self.sample_one_metadata(self.SAMPLE_ONE).model_copy(deep=True)
        new_metadata.SourceFile = new_sample_one
        new_metadata.RegionInfo.RegionList[0].Name = "Billy Bob"

        write_image_metadata(new_metadata)

        changed_metadata = read_image_metadata(new_sample_one)

        self.verify_expected_vs_actual_metadata(new_metadata, changed_metadata)

    def test_bulk_write_faces(self, temporary_directory: Path):

        new_sample_one = Path(shutil.copy(self.SAMPLE_ONE, temporary_directory / self.SAMPLE_ONE.name))
        new_sample_two = Path(shutil.copy(self.SAMPLE_TWO, temporary_directory / self.SAMPLE_TWO.name))

        old_one_metadata = self.sample_one_metadata(self.SAMPLE_ONE)
        old_two_metadata = self.sample_two_metadata(self.SAMPLE_TWO)

        new_one_metadata = old_one_metadata.model_copy(deep=True)
        new_one_metadata.SourceFile = new_sample_one

        new_two_metadata = old_two_metadata.model_copy(deep=True)
        new_two_metadata.SourceFile = new_sample_two
        new_two_metadata.RegionInfo.RegionList[0].Area = XmpAreaStruct(
            H=0.1,
            Unit="normalized",
            W=0.2,
            X=0.3,
            Y=0.4,
            D=None,
        )

        bulk_write_image_metadata([new_one_metadata, new_two_metadata])

        changed_metadata = bulk_read_image_metadata([new_sample_one, new_sample_two])

        assert len(changed_metadata) == 2

        self.verify_expected_vs_actual_metadata(new_one_metadata, changed_metadata[0])
        self.verify_expected_vs_actual_metadata(new_two_metadata, changed_metadata[1])

    def test_write_change_keywords(self, temporary_directory: Path):

        new_sample_one = Path(shutil.copy(self.SAMPLE_ONE, temporary_directory / self.SAMPLE_ONE.name))

        new_metadata = self.sample_one_metadata(self.SAMPLE_ONE).model_copy(deep=True)
        new_metadata.SourceFile = new_sample_one
        # Clear all the old style tags
        new_metadata.RegionInfo = None
        new_metadata.HierarchicalSubject = None
        new_metadata.CatalogSets = None
        new_metadata.TagsList = None
        new_metadata.LastKeywordXMP = None
        # Construct a new tree
        new_metadata.KeywordInfo = KeywordInfoModel(
            Hierarchy=[
                KeywordStruct(
                    Keyword="New Root Tag",
                    Children=[KeywordStruct(Keyword="New Child Tag", Children=[])],
                ),
            ],
        )

        write_image_metadata(new_metadata, clear_existing_metadata=True)

        changed_metadata = read_image_metadata(new_sample_one)

        # TODO: CatalogSets is returned empty for some reason
        # new_metadata.CatalogSets = None

        self.verify_expected_vs_actual_metadata(new_metadata, changed_metadata)

    def test_write_change_no_keywords(self, temporary_directory: Path):

        new_sample_one = Path(shutil.copy(self.SAMPLE_ONE, temporary_directory / self.SAMPLE_ONE.name))

        new_metadata = self.sample_one_metadata(self.SAMPLE_ONE).model_copy(deep=True)
        new_metadata.SourceFile = new_sample_one
        # Clear all the tags
        new_metadata.RegionInfo = None
        new_metadata.HierarchicalSubject = None
        new_metadata.CatalogSets = None
        new_metadata.TagsList = None
        new_metadata.LastKeywordXMP = None
        new_metadata.KeywordInfo = None

        write_image_metadata(new_metadata, clear_existing_metadata=True)

        changed_metadata = read_image_metadata(new_sample_one)

        self.verify_expected_vs_actual_metadata(new_metadata, changed_metadata)


class TestMetadataClear(SampleMetadataMixin, SampleDirMixin):
    def test_clear_existing_metadata(self, temporary_directory: Path):

        new_sample_one = Path(shutil.copy(self.SAMPLE_ONE, temporary_directory / self.SAMPLE_ONE.name))

        # Everything should be cleared
        expected = self.sample_one_metadata(new_sample_one).model_copy(deep=True)
        expected.RegionInfo = None
        expected.LastKeywordXMP = None
        expected.CatalogSets = None
        expected.TagsList = None
        expected.HierarchicalSubject = None
        expected.KeywordInfo = None
        expected.Description = None

        clear_existing_metadata(new_sample_one)

        changed_metadata = read_image_metadata(new_sample_one)

        self.verify_expected_vs_actual_metadata(expected, changed_metadata)


class TestErrorCases:
    def test_write_no_images(self):
        with pytest.raises(NoImageMetadataError):
            bulk_write_image_metadata([])

    def test_read_no_images(self):
        with pytest.raises(NoImagePathsError):
            bulk_read_image_metadata([])

    def test_not_a_file(self):
        with pytest.raises(FileNotFoundError):
            bulk_read_image_metadata([Path("not-a-path")])

    def test_is_a_dir(self, temporary_directory: Path):
        with pytest.raises(ImagePathNotFileError):
            bulk_read_image_metadata([temporary_directory])
