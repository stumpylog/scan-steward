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
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import KeywordInfoModel
from scansteward.imageops.models import KeywordStruct
from scansteward.imageops.models import XmpAreaStruct
from scansteward.tests.mixins import MetadataVerifyMixin


class TestReadImageMetadata(MetadataVerifyMixin):
    def test_read_single_image_metadata(self, sample_one_original_file: Path, sample_one_metadata_copy: ImageMetadata):
        metadata = read_image_metadata(sample_one_original_file)

        sample_one_metadata_copy.SourceFile = sample_one_original_file

        self.verify_expected_vs_actual_metadata(sample_one_metadata_copy, metadata)

    def test_bulk_read_image_metadata(
        self,
        sample_one_original_file: Path,
        sample_two_original_file: Path,
        sample_one_metadata_copy: ImageMetadata,
        sample_two_metadata_copy: ImageMetadata,
    ):
        metadata = bulk_read_image_metadata(
            [sample_one_original_file, sample_two_original_file],
        )

        sample_one_metadata_copy.SourceFile = sample_one_original_file
        sample_two_metadata_copy.SourceFile = sample_two_original_file

        assert len(metadata) == 2

        self.verify_expected_vs_actual_metadata(sample_one_metadata_copy, metadata[0])
        self.verify_expected_vs_actual_metadata(sample_two_metadata_copy, metadata[1])


class TestWriteImageMetadata(MetadataVerifyMixin):
    def test_change_single_image_metadata(self, sample_one_metadata_copy: ImageMetadata):
        # Change something
        sample_one_metadata_copy.RegionInfo.RegionList[0].Name = "Billy Bob"

        write_image_metadata(sample_one_metadata_copy)

        changed_metadata = read_image_metadata(sample_one_metadata_copy.SourceFile)

        self.verify_expected_vs_actual_metadata(sample_one_metadata_copy, changed_metadata)

    def test_bulk_write_faces(self, sample_one_metadata_copy: ImageMetadata, sample_two_metadata_copy: ImageMetadata):
        # Change the name of the first face in sample one
        sample_one_metadata_copy.RegionInfo.RegionList[0].Name = "Billy Bob"

        # Change the name and location of the first face in sample two
        sample_two_metadata_copy.RegionInfo.RegionList[0].Name = "Sally Sue"
        sample_two_metadata_copy.RegionInfo.RegionList[0].Area = XmpAreaStruct(
            H=0.1,
            Unit="normalized",
            W=0.2,
            X=0.3,
            Y=0.4,
            D=None,
        )

        bulk_write_image_metadata([sample_one_metadata_copy, sample_two_metadata_copy])

        changed_metadata = bulk_read_image_metadata(
            [sample_one_metadata_copy.SourceFile, sample_two_metadata_copy.SourceFile],
        )

        assert len(changed_metadata) == 2

        self.verify_expected_vs_actual_metadata(sample_one_metadata_copy, changed_metadata[0])
        self.verify_expected_vs_actual_metadata(sample_two_metadata_copy, changed_metadata[1])

    def test_write_change_keywords(
        self,
        sample_one_metadata_copy: ImageMetadata,
    ):
        # Clear all the old style tags
        sample_one_metadata_copy.RegionInfo = None
        sample_one_metadata_copy.HierarchicalSubject = None
        sample_one_metadata_copy.CatalogSets = None
        sample_one_metadata_copy.TagsList = None
        sample_one_metadata_copy.LastKeywordXMP = None
        # Construct a new tree
        sample_one_metadata_copy.KeywordInfo = KeywordInfoModel(
            Hierarchy=[
                KeywordStruct(
                    Keyword="New Root Tag",
                    Children=[KeywordStruct(Keyword="New Child Tag", Children=[])],
                ),
            ],
        )

        write_image_metadata(sample_one_metadata_copy, clear_existing_metadata=True)

        changed_metadata = read_image_metadata(sample_one_metadata_copy.SourceFile)

        # TODO: CatalogSets is returned empty for some reason
        sample_one_metadata_copy.CatalogSets = None

        self.verify_expected_vs_actual_metadata(sample_one_metadata_copy, changed_metadata)

    def test_write_change_no_keywords(
        self,
        sample_one_metadata_copy: ImageMetadata,
    ):
        # Clear all the tags
        sample_one_metadata_copy.RegionInfo = None
        sample_one_metadata_copy.HierarchicalSubject = None
        sample_one_metadata_copy.CatalogSets = None
        sample_one_metadata_copy.TagsList = None
        sample_one_metadata_copy.LastKeywordXMP = None
        sample_one_metadata_copy.KeywordInfo = None

        write_image_metadata(sample_one_metadata_copy, clear_existing_metadata=True)

        changed_metadata = read_image_metadata(sample_one_metadata_copy.SourceFile)

        self.verify_expected_vs_actual_metadata(sample_one_metadata_copy, changed_metadata)

    def test_update_single_value(self, sample_one_metadata_copy: ImageMetadata):
        sample_one_metadata_copy.Title = "This is a new Title"

        write_image_metadata(sample_one_metadata_copy)

        changed_metadata = read_image_metadata(sample_one_metadata_copy.SourceFile)

        self.verify_expected_vs_actual_metadata(sample_one_metadata_copy, changed_metadata)


class TestMetadataClear(MetadataVerifyMixin):
    def test_clear_existing_metadata(self, sample_three_metadata_copy: ImageMetadata):
        # Everything should be cleared (except SourceFile, obviously)
        expected = ImageMetadata(SourceFile=sample_three_metadata_copy.SourceFile)

        clear_existing_metadata(sample_three_metadata_copy.SourceFile)

        changed_metadata = read_image_metadata(sample_three_metadata_copy.SourceFile)

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

    def test_is_a_dir(self, tmp_path: Path):
        with pytest.raises(ImagePathNotFileError):
            bulk_read_image_metadata([tmp_path])
