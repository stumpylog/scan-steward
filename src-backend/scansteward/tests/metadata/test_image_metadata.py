import collections
import shutil
from pathlib import Path

import pytest

from scansteward.imageops.errors import ImagePathNotFileError
from scansteward.imageops.errors import NoImageMetadataError
from scansteward.imageops.errors import NoImagePathsError
from scansteward.imageops.metadata import bulk_read_image_metadata
from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.metadata import read_image_metadata
from scansteward.imageops.metadata import write_image_metadata, clear_existing_metadata
from scansteward.imageops.models import DimensionsStruct
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import KeywordInfoModel
from scansteward.imageops.models import KeywordStruct
from scansteward.imageops.models import RegionInfoStruct
from scansteward.imageops.models import RegionStruct
from scansteward.imageops.models import RotationEnum
from scansteward.imageops.models import XmpAreaStruct


def assert_count_equal(first: list | None, second: list | None) -> None:
    """
    https://github.com/python/cpython/blob/17d31bf3843c384873999a15ce683cc3654f46ae/Lib/unittest/case.py#L1186
    """
    first_seq, second_seq = list(first or []), list(second or [])
    first_counter = collections.Counter(first_seq)
    second_counter = collections.Counter(second_seq)
    assert first_counter == second_counter


def verify_expected_vs_actual_metadata(expected: ImageMetadata, actual: ImageMetadata):
    assert expected.SourceFile == actual.SourceFile
    assert expected.Title == actual.Title
    assert expected.Description == actual.Description
    assert expected.RegionInfo == actual.RegionInfo
    assert expected.Orientation == actual.Orientation
    assert_count_equal(expected.LastKeywordXMP, actual.LastKeywordXMP)
    assert_count_equal(expected.TagsList, actual.TagsList)
    assert_count_equal(expected.CatalogSets, actual.CatalogSets)
    assert_count_equal(expected.HierarchicalSubject, actual.HierarchicalSubject)
    assert expected.KeywordInfo == actual.KeywordInfo


def sample_one_metadata(sample_one_jpeg: Path) -> ImageMetadata:
    list_of_tags = [
        ["Locations", "United States", "Washington DC"],
        ["People", "Barack Obama"],
        ["Pets", "Dogs", "Bo"],
    ]
    return ImageMetadata(
        SourceFile=sample_one_jpeg,
        Title=None,
        Description=(
            "President Barack Obama throws a ball for Bo, the family dog, in the Rose Garden"
            " of the White House, Sept. 9, 2010.  (Official White House Photo by Pete Souza)\n\nThis official White"
            " House photograph is being made available only for publication by news organizations and/or for personal"
            " use printing by the subject(s) of the photograph. The photograph may not be manipulated in any way and"
            " may not be used in commercial or political materials, advertisements, emails, products, promotions that"
            " in any way suggests approval or endorsement of the President, the First Family, or the White House. "
        ),
        RegionInfo=RegionInfoStruct(
            AppliedToDimensions=DimensionsStruct(H=683.0, W=1024.0, Unit="pixel"),
            RegionList=[
                RegionStruct(
                    Area=XmpAreaStruct(
                        H=0.0585652,
                        W=0.0292969,
                        X=0.317383,
                        Y=0.303075,
                        Unit="normalized",
                        D=None,
                    ),
                    Name="Barack Obama",
                    Type="Face",
                    Description=None,
                ),
            ],
        ),
        Orientation=None,
        LastKeywordXMP=["/".join(x) for x in list_of_tags],
        TagsList=["/".join(x) for x in list_of_tags],
        CatalogSets=["|".join(x) for x in list_of_tags],
        HierarchicalSubject=["|".join(x) for x in list_of_tags],
        # This is the expected tree from the tags
        KeywordInfo=KeywordInfoModel.model_validate(
            {
                "Hierarchy": [
                    {
                        "Applied": None,
                        "Children": [
                            {
                                "Applied": None,
                                "Children": [{"Applied": None, "Children": [], "Keyword": "Bo"}],
                                "Keyword": "Dogs",
                            },
                        ],
                        "Keyword": "Pets",
                    },
                    {
                        "Applied": None,
                        "Children": [
                            {
                                "Applied": None,
                                "Children": [{"Applied": None, "Children": [], "Keyword": "Washington DC"}],
                                "Keyword": "United States",
                            },
                        ],
                        "Keyword": "Locations",
                    },
                    {
                        "Applied": None,
                        "Children": [{"Applied": None, "Children": [], "Keyword": "Barack Obama"}],
                        "Keyword": "People",
                    },
                ],
            },
        ),
    )


def sample_two_metadata(sample_two_jpeg: Path) -> ImageMetadata:
    list_of_tags = [["Locations", "United States", "Washington DC"], ["People", "Barack Obama"]]
    return ImageMetadata(
        SourceFile=sample_two_jpeg,
        Title=None,
        Description=(
            "President Barack Obama signs a letter to a Cuban letter writer, in the Oval Office, March 14, 2016."
            " (Official White House Photo by Pete Souza)\n\nThis official White House photograph is being made"
            " available only for publication by news organizations and/or for personal use printing by the"
            " subject(s) of the photograph. The photograph may not be manipulated in any way and may not be"
            " used in commercial or political materials, advertisements, emails, products, promotions that"
            " in any way suggests approval or endorsement of the President, the First Family, or the White House."
        ),
        RegionInfo=RegionInfoStruct(
            AppliedToDimensions=DimensionsStruct(H=2333.0, W=3500.0, Unit="pixel"),
            RegionList=[
                RegionStruct(
                    Area=XmpAreaStruct(
                        H=0.216459,
                        Unit="normalized",
                        W=0.129714,
                        X=0.492857,
                        Y=0.277968,
                        D=None,
                    ),
                    Name="Barack Obama",
                    Type="Face",
                    Description=None,
                ),
            ],
        ),
        Orientation=RotationEnum.HORIZONTAL,
        LastKeywordXMP=["/".join(x) for x in list_of_tags],
        TagsList=["/".join(x) for x in list_of_tags],
        CatalogSets=["|".join(x) for x in list_of_tags],
        HierarchicalSubject=["|".join(x) for x in list_of_tags],
        # This is the expected tree from the tags
        KeywordInfo=KeywordInfoModel.model_validate(
            {
                "Hierarchy": [
                    {
                        "Applied": None,
                        "Children": [
                            {
                                "Applied": None,
                                "Children": [{"Applied": None, "Children": [], "Keyword": "Washington DC"}],
                                "Keyword": "United States",
                            },
                        ],
                        "Keyword": "Locations",
                    },
                    {
                        "Applied": None,
                        "Children": [{"Applied": None, "Children": [], "Keyword": "Barack Obama"}],
                        "Keyword": "People",
                    },
                ],
            },
        ),
    )


def verify_sample_one_metadata(sample_one_jpeg: Path, actual: ImageMetadata) -> None:
    expected = sample_one_metadata(sample_one_jpeg)
    verify_expected_vs_actual_metadata(expected=expected, actual=actual)


def verify_sample_two_metadata(sample_two_jpeg: Path, actual: ImageMetadata) -> None:
    expected = sample_two_metadata(sample_two_jpeg)
    verify_expected_vs_actual_metadata(expected=expected, actual=actual)


class TestReadImageMetadata:

    def test_read_single_image_metadata(self, sample_one_jpeg: Path):

        metadata = read_image_metadata(sample_one_jpeg)

        verify_sample_one_metadata(sample_one_jpeg, metadata)

    def test_bulk_read_image_faces(self, sample_one_jpeg: Path, sample_two_jpeg: Path):
        metadata = bulk_read_image_metadata(
            [sample_one_jpeg, sample_two_jpeg],
        )

        assert len(metadata) == 2

        verify_sample_one_metadata(sample_one_jpeg, metadata[0])
        verify_sample_two_metadata(sample_two_jpeg, metadata[1])


class TestWriteImageMetadata:
    def test_change_single_image_metadata(self, temporary_directory: Path, sample_one_jpeg: Path):

        new_sample_one = Path(shutil.copy(sample_one_jpeg, temporary_directory / sample_one_jpeg.name))

        # Change something
        new_metadata = sample_one_metadata(sample_one_jpeg).model_copy(deep=True)
        new_metadata.SourceFile = new_sample_one
        new_metadata.RegionInfo.RegionList[0].Name = "Billy Bob"

        write_image_metadata(new_metadata)

        changed_metadata = read_image_metadata(new_sample_one)

        verify_expected_vs_actual_metadata(new_metadata, changed_metadata)

    def test_bulk_write_faces(self, temporary_directory: Path, sample_one_jpeg: Path, sample_two_jpeg: Path):

        new_sample_one = Path(shutil.copy(sample_one_jpeg, temporary_directory / sample_one_jpeg.name))
        new_sample_two = Path(shutil.copy(sample_two_jpeg, temporary_directory / sample_two_jpeg.name))

        old_one_metadata = sample_one_metadata(sample_one_jpeg)
        old_two_metadata = sample_two_metadata(sample_two_jpeg)

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

        verify_expected_vs_actual_metadata(new_one_metadata, changed_metadata[0])
        verify_expected_vs_actual_metadata(new_two_metadata, changed_metadata[1])

    def test_write_change_keywords(self, temporary_directory: Path, sample_one_jpeg: Path):

        new_sample_one = Path(shutil.copy(sample_one_jpeg, temporary_directory / sample_one_jpeg.name))

        new_metadata = sample_one_metadata(sample_one_jpeg).model_copy(deep=True)
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

        shutil.copy(new_sample_one, sample_one_jpeg.parent / "before.jpeg")

        write_image_metadata(new_metadata, clear_existing_metadata=True)

        shutil.copy(new_sample_one, sample_one_jpeg.parent / "after.jpeg")

        changed_metadata = read_image_metadata(new_sample_one)

        # TODO: CatalogSets is returned empty for some reason
        # new_metadata.CatalogSets = None

        verify_expected_vs_actual_metadata(new_metadata, changed_metadata)

    def test_write_change_no_keywords(self, temporary_directory: Path, sample_one_jpeg: Path):

        new_sample_one = Path(shutil.copy(sample_one_jpeg, temporary_directory / sample_one_jpeg.name))

        new_metadata = sample_one_metadata(sample_one_jpeg).model_copy(deep=True)
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

        verify_expected_vs_actual_metadata(new_metadata, changed_metadata)


class TestMetadataClear:
    def test_clear_existing_metadata(self, temporary_directory: Path, sample_one_jpeg: Path):

        new_sample_one = Path(shutil.copy(sample_one_jpeg, temporary_directory / sample_one_jpeg.name))

        clear_existing_metadata(new_sample_one)

        changed_metadata = read_image_metadata(new_sample_one)

        # Everything should be cleared
        expected = sample_one_metadata(new_sample_one).model_copy(deep=True)
        expected.RegionInfo = None
        expected.LastKeywordXMP = None
        expected.CatalogSets = None
        expected.TagsList = None
        expected.HierarchicalSubject = None
        expected.KeywordInfo = None
        expected.Description = None

        verify_expected_vs_actual_metadata(expected, changed_metadata)


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
