import collections
import shutil
import tempfile
from collections.abc import Sequence
from contextlib import ExitStack
from contextlib import contextmanager
from pathlib import Path
from typing import Final

from django.core.management import call_command
from django.db import models
from django.test import override_settings

from scansteward.imageops.models import ImageMetadata
from scansteward.models import Image
from scansteward.models import Person
from scansteward.models import Pet
from scansteward.models import RoughDate
from scansteward.models import RoughLocation
from scansteward.signals.handlers import mark_image_as_dirty
from scansteward.signals.handlers import mark_images_as_dirty_on_fk_change
from scansteward.signals.handlers import mark_images_as_dirty_on_m2m_change


@contextmanager
def disable_signal(sig, receiver, sender):
    try:
        sig.disconnect(receiver=receiver, sender=sender)
        yield
    finally:
        sig.connect(receiver=receiver, sender=sender)


class TemporaryDirectoryMixin:
    """
    Provides a helper which will generate new temporary directories as needed,
    which will all be removed when the class is torn down

    Test functions can also use the temporary_directory fixture, but this is
    not accessible in the setup/teardown methods or other utility type functions.

    It also does not work with Django's TestCase
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
        self.BASE_DIR = self.get_new_temporary_dir()
        self.DATA_DIR = self.BASE_DIR / "data"
        self.LOGS_DIR = self.DATA_DIR / "logs"
        self.MEDIA_DIR = self.BASE_DIR / "media"
        self.THUMBNAIL_DIR = self.MEDIA_DIR / "thumbnails"
        self.FULL_SIZE_DIR = self.MEDIA_DIR / "fullsize"
        for x in [self.DATA_DIR, self.LOGS_DIR, self.MEDIA_DIR, self.THUMBNAIL_DIR, self.FULL_SIZE_DIR]:
            x.mkdir(parents=True)
        self._overrides = override_settings(
            BASE_DIR=self.BASE_DIR,
            DATA_DIR=self.DATA_DIR,
            LOGGING_DIR=self.LOGS_DIR,
            MEDIA_ROOT=self.MEDIA_DIR,
            THUMBNAIL_DIR=self.THUMBNAIL_DIR,
            FULL_SIZE_DIR=self.FULL_SIZE_DIR,
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
    SAMPLE_DIR: Final = Path(__file__).parent / "samples"

    IMAGE_SAMPLE_DIR: Final = SAMPLE_DIR / "images"

    SAMPLE_ORIGINALS_IMAGE_DIR: Final = IMAGE_SAMPLE_DIR / "originals"
    SAMPLE_THUMBNAIL_IMAGE_DIR: Final = IMAGE_SAMPLE_DIR / "thumbnails"
    SAMPLE_FULLSIZE_IMAGE_DIR: Final = IMAGE_SAMPLE_DIR / "fullsize"

    SAMPLE_ONE: Final = SAMPLE_ORIGINALS_IMAGE_DIR / "sample1.jpg"
    SAMPLE_TWO: Final = SAMPLE_ORIGINALS_IMAGE_DIR / "sample2.jpg"
    SAMPLE_THREE: Final = SAMPLE_ORIGINALS_IMAGE_DIR / "sample3.jpg"
    SAMPLE_FOUR: Final = SAMPLE_ORIGINALS_IMAGE_DIR / "sample4.jpg"

    ALL_SAMPLE_IMAGES: Final[Sequence[Path]] = [SAMPLE_ONE, SAMPLE_TWO, SAMPLE_THREE, SAMPLE_FOUR]


class FixtureDirMixin:
    FIXTURE_DIR = Path(__file__).parent / "fixtures"
    SAMPLE_IMAGE_DB_FIXTURE = FIXTURE_DIR / "indexed_sample_database.json"


class SampleMetadataMixin(FixtureDirMixin):
    """
    Utilities for verifying sample image metadata and metadata in general against itself


    The expected metadata is loaded once from a fixture file which was dumped via Pydantic
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
        if not hasattr(self, "SAMPLE_ONE_METADATA"):
            self.SAMPLE_ONE_METADATA = ImageMetadata.model_validate_json(
                (self.FIXTURE_DIR / "sample1.jpg.json").read_text(),
            )
        cpy = self.SAMPLE_ONE_METADATA.model_copy(deep=True)
        cpy.SourceFile = sample_one_jpeg
        return cpy

    def sample_two_metadata(self, sample_two_jpeg: Path) -> ImageMetadata:
        if not hasattr(self, "SAMPLE_TWO_METADATA"):
            self.SAMPLE_TWO_METADATA = ImageMetadata.model_validate_json(
                (self.FIXTURE_DIR / "sample2.jpg.json").read_text(),
            )
        cpy = self.SAMPLE_TWO_METADATA.model_copy(deep=True)
        cpy.SourceFile = sample_two_jpeg
        return cpy

    def sample_three_metadata(self, sample_three_jpeg: Path) -> ImageMetadata:
        if not hasattr(self, "SAMPLE_THREE_METADATA"):
            self.SAMPLE_THREE_METADATA = ImageMetadata.model_validate_json(
                (self.FIXTURE_DIR / "sample3.jpg.json").read_text(),
            )
        cpy = self.SAMPLE_THREE_METADATA.model_copy(deep=True)
        cpy.SourceFile = sample_three_jpeg
        return cpy

    def sample_four_metadata(self, sample_four_jpeg: Path) -> ImageMetadata:
        if not hasattr(self, "SAMPLE_FOUR_METADATA"):
            self.SAMPLE_FOUR_METADATA = ImageMetadata.model_validate_json(
                (self.FIXTURE_DIR / "sample4.jpg.json").read_text(),
            )
        cpy = self.SAMPLE_FOUR_METADATA.model_copy(deep=True)
        cpy.SourceFile = sample_four_jpeg
        return cpy

    def verify_sample_one_metadata(self, sample_one_jpeg: Path, actual: ImageMetadata) -> None:
        expected = self.sample_one_metadata(sample_one_jpeg)
        self.verify_expected_vs_actual_metadata(expected=expected, actual=actual)

    def verify_sample_two_metadata(self, sample_two_jpeg: Path, actual: ImageMetadata) -> None:
        expected = self.sample_two_metadata(sample_two_jpeg)
        self.verify_expected_vs_actual_metadata(expected=expected, actual=actual)


class IndexedEnvironmentMixin(SampleDirMixin, FixtureDirMixin, DirectoriesMixin):
    """
    Constructs the environment for an already indexed directory of all the sample files.

    This does the following:
      - Load a pre-constructed JSON fixture to the database
      - Copy sample original file to correct (overridden) directory
      - Copy sample fullsize file to correct (overridden) directory
      - Copy sample thumbnail file to correct (overridden) directory

    For speed, this does not actually call index, but rather just constructs the environment with fixed,
    known values.
    """

    SAMPLE_ONE_PK: Final[int] = 1

    def setUp(self) -> None:
        # Create directories and override settings
        super().setUp()

        # Load the database
        with (
            disable_signal(models.signals.post_save, mark_image_as_dirty, Image),
            disable_signal(models.signals.post_save, mark_images_as_dirty_on_m2m_change, Pet),
            disable_signal(models.signals.post_save, mark_images_as_dirty_on_m2m_change, Person),
            disable_signal(models.signals.post_save, mark_images_as_dirty_on_fk_change, RoughLocation),
            disable_signal(models.signals.post_save, mark_images_as_dirty_on_fk_change, RoughDate),
        ):
            call_command("loaddata", str(self.SAMPLE_IMAGE_DB_FIXTURE))

        # Copy the files
        for pk in range(1, 5):
            img = Image.objects.get(pk=pk)

            # The original needs to be updated
            img.original_path = shutil.copy(
                self.SAMPLE_ORIGINALS_IMAGE_DIR / img.original_path.name,
                self.BASE_DIR / img.original_path.name,
            )
            img.save()
            img.mark_as_clean()

            shutil.copy(
                self.SAMPLE_FULLSIZE_IMAGE_DIR / img.full_size_path.name,
                img.full_size_path,
            )
            shutil.copy(
                self.SAMPLE_THUMBNAIL_IMAGE_DIR / img.thumbnail_path.name,
                img.thumbnail_path,
            )
