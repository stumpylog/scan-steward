import collections
import tempfile
from collections.abc import Sequence
from contextlib import ExitStack
from pathlib import Path

from django.test import override_settings

from scansteward.imageops.models import DimensionsStruct
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import KeywordInfoModel
from scansteward.imageops.models import RegionInfoStruct
from scansteward.imageops.models import RegionStruct
from scansteward.imageops.models import RotationEnum
from scansteward.imageops.models import XmpAreaStruct


class TemporaryDirectoryMixin:
    """
    Provides a helper which will generate new temporary directories as needed,
    which will all be removed when the class is torn down
    """

    @classmethod
    def setUpClass(cls):
        cls._dir_stack = ExitStack()  # type: ignore[attr-defined]
        super().setUpClass()  # type: ignore[misc]

    @classmethod
    def tearDownClass(cls) -> None:
        cls._dir_stack.close()  # type: ignore[attr-defined]
        super().tearDownClass()  # type: ignore[misc]

    def get_new_temporary_dir(self) -> Path:
        """
        Generates a new temporary directory which will be cleaned up on tearDown
        """
        tmp_dir = self._dir_stack.enter_context(tempfile.TemporaryDirectory(ignore_cleanup_errors=True))  # type: ignore[attr-defined]
        return Path(tmp_dir)


class DirectoriesMixin(TemporaryDirectoryMixin):
    """
    Creates and overrides settings for all folders and paths defined, then ensures
    they are cleaned up on exit
    """

    def setUp(self) -> None:
        super().setUp()  # type: ignore[misc] - This is defined for TestCase
        base_dir = self.get_new_temporary_dir()
        data = base_dir / "data"
        logs = data / "logs"
        media = base_dir / "media"
        thumbnail = media / "thumbnails"
        fullsize = media / "fullsize"
        for x in [data, logs, media, thumbnail, fullsize]:
            x.mkdir(parents=True)
        self._overrides = override_settings(
            BASE_DIR=base_dir,
            DATA_DIR=data,
            LOGGING_DIR=logs,
            MEDIA_ROOT=media,
            THUMBNAIL_DIR=thumbnail,
            FULL_SIZE_DIR=fullsize,
        )
        self._overrides.enable()

    def tearDown(self) -> None:
        super().tearDown()  # type: ignore[misc] - This is defined for TestCase
        self._overrides.disable()


class FileSystemAssertsMixin:
    """
    Utilities for checks various state information of the file system
    """

    def assertIsFile(self, path: Path | str):  # noqa: N802
        assert Path(path).resolve().is_file(), f"File does not exist: {path}"

    def assertIsNotFile(self, path: Path | str):  # noqa: N802
        assert not Path(path).resolve().is_file(), f"File does exist: {path}"

    def assertIsDir(self, path: Path | str):  # noqa: N802
        assert Path(path).resolve().is_dir(), f"Dir does not exist: {path}"

    def assertIsNotDir(self, path: Path | str):  # noqa: N802
        assert not Path(path).resolve().is_dir(), f"Dir does exist: {path}"

    def assertFilesEqual(  # noqa: N802
        self,
        path1: Path | str,
        path2: Path | str,
    ):
        path1 = Path(path1)
        path2 = Path(path2)
        import hashlib

        hash1 = hashlib.sha256(path1.read_bytes()).hexdigest()
        hash2 = hashlib.sha256(path2.read_bytes()).hexdigest()

        assert hash1 == hash2, "File SHA256 mismatch"

    def assertFileContents(self, file: Path | str, content: bytes | bytearray):  # noqa: N802
        file = Path(file)
        self.assertIsFile(file)

        actual_content = file.read_bytes()
        assert actual_content == content


class SampleDirMixin:
    SAMPLE_DIR = Path(__file__).parent / "samples"
    IMAGE_SAMPLE_DIR = SAMPLE_DIR / "images"
    SAMPLE_ONE = IMAGE_SAMPLE_DIR / "sample1.jpg"
    SAMPLE_TWO = IMAGE_SAMPLE_DIR / "sample2.jpg"
    SAMPLE_THREE = IMAGE_SAMPLE_DIR / "sample3.jpg"
    SAMPLE_FOUR = IMAGE_SAMPLE_DIR / "sample4.jpg"
    ALL_SAMPLE_IMAGES: Sequence[Path] = [SAMPLE_ONE, SAMPLE_TWO, SAMPLE_THREE, SAMPLE_FOUR]


class SampleMetadataMixin:
    """
    Utilities for verifing sample image metadata and metadata in general against itself
    """

    def assert_count_equal(self, expected: list[str | int] | None, actual: list[str | int] | None) -> None:
        """
        https://github.com/python/cpython/blob/17d31bf3843c384873999a15ce683cc3654f46ae/Lib/unittest/case.py#L1186
        """
        expected_seq, actual_seq = list(expected or []), list(actual or [])
        expected_counter = collections.Counter(expected_seq)
        actual_counter = collections.Counter(actual_seq)
        assert expected_counter == actual_counter

    def verify_expected_vs_actual_metadata(self, expected: ImageMetadata, actual: ImageMetadata):
        assert expected.SourceFile == actual.SourceFile
        assert expected.Title == actual.Title
        assert expected.Description == actual.Description

        if expected.RegionInfo is None or actual.RegionInfo is None:
            assert expected.RegionInfo == actual.RegionInfo
        else:
            assert expected.RegionInfo.model_dump() == actual.RegionInfo.model_dump()

        assert expected.Orientation == actual.Orientation
        self.assert_count_equal(expected.LastKeywordXMP, actual.LastKeywordXMP)
        self.assert_count_equal(expected.TagsList, actual.TagsList)
        self.assert_count_equal(expected.CatalogSets, actual.CatalogSets)
        self.assert_count_equal(expected.HierarchicalSubject, actual.HierarchicalSubject)
        if expected.KeywordInfo is None or actual.KeywordInfo is None:
            assert expected.KeywordInfo == actual.KeywordInfo
        else:
            assert expected.KeywordInfo.model_dump() == actual.KeywordInfo.model_dump()

    def sample_one_metadata(self, sample_one_jpeg: Path) -> ImageMetadata:
        list_of_tags = [
            ["Locations", "United States", "District of Columbia", "Washington DC"],
            ["People", "Barack Obama"],
            ["Pets", "Dogs", "Bo"],
            ["Dates", "2010", "09 - September", "9"],
        ]
        return ImageMetadata(
            SourceFile=sample_one_jpeg,
            ImageHeight=683,
            ImageWidth=1024,
            Title=None,
            Description=(
                "President Barack Obama throws a ball for Bo, the family dog,"
                " in the Rose Garden of the White House, Sept. 9, 2010. "
                " (Official White House Photo by Pete Souza)"
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
                    RegionStruct(
                        Area=XmpAreaStruct(
                            H=0.284041,
                            W=0.202148,
                            X=0.616699,
                            Y=0.768668,
                            Unit="normalized",
                            D=None,
                        ),
                        Name="Bo",
                        Type="Pet",
                        Description="Bo was a pet dog of the Obama family",
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
                            "Keyword": "People",
                            "Applied": None,
                            "Children": [{"Applied": None, "Children": [], "Keyword": "Barack Obama"}],
                        },
                        {
                            "Keyword": "Locations",
                            "Applied": None,
                            "Children": [
                                {
                                    "Keyword": "United States",
                                    "Applied": None,
                                    "Children": [
                                        {
                                            "Keyword": "District of Columbia",
                                            "Applied": None,
                                            "Children": [
                                                {
                                                    "Keyword": "Washington DC",
                                                    "Applied": None,
                                                    "Children": [],
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "Keyword": "Dates",
                            "Applied": None,
                            "Children": [
                                {
                                    "Keyword": "2010",
                                    "Applied": None,
                                    "Children": [
                                        {
                                            "Keyword": "09 - September",
                                            "Applied": None,
                                            "Children": [{"Applied": None, "Children": [], "Keyword": "9"}],
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "Keyword": "Pets",
                            "Applied": None,
                            "Children": [
                                {
                                    "Keyword": "Dogs",
                                    "Applied": None,
                                    "Children": [{"Applied": None, "Children": [], "Keyword": "Bo"}],
                                },
                            ],
                        },
                    ],
                },
            ),
            City="WASHINGTON",
            Country="USA",
        )

    def sample_two_metadata(self, sample_two_jpeg: Path) -> ImageMetadata:
        list_of_tags = [["Locations", "United States", "Washington DC"], ["People", "Barack Obama"]]
        return ImageMetadata(
            SourceFile=sample_two_jpeg,
            ImageHeight=2333,
            ImageWidth=3500,
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
                                    "Children": [
                                        {"Applied": None, "Children": [], "Keyword": "Washington DC"},
                                    ],
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

    def verify_sample_one_metadata(self, sample_one_jpeg: Path, actual: ImageMetadata) -> None:
        expected = self.sample_one_metadata(sample_one_jpeg)
        self.verify_expected_vs_actual_metadata(expected=expected, actual=actual)

    def verify_sample_two_metadata(self, sample_two_jpeg: Path, actual: ImageMetadata) -> None:
        expected = self.sample_two_metadata(sample_two_jpeg)
        self.verify_expected_vs_actual_metadata(expected=expected, actual=actual)
