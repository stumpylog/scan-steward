import shutil
from pathlib import Path

from scansteward.imageops.metadata import bulk_read_image_metadata
from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.metadata import read_image_metadata
from scansteward.imageops.metadata import write_image_metadata
from scansteward.imageops.models import DimensionsStruct
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import KeywordInfoModel
from scansteward.imageops.models import RegionInfoStruct
from scansteward.imageops.models import RegionStruct
from scansteward.imageops.models import RotationEnum
from scansteward.imageops.models import XmpAreaStruct


def assert_count_equal(list_one: list | None, list_two: list | None) -> None:
    list_one = list_one if list_one else []
    list_two = list_two if list_two else []
    difference = set(list_one) ^ set(list_two)
    assert not difference


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


class TestWriteImageMetdata:
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
