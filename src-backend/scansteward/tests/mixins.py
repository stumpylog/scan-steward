import collections
import tempfile
from contextlib import ExitStack
from pathlib import Path

from django.test import override_settings

from scansteward.imageops.models import ImageMetadata


class TemporaryDirectoryMixin:
    """
    Provides a helper which will generate new temporary directories as needed,
    which will all be removed when the class is torn down

    Test functions can also use the tmp_path fixture, but this is
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


class MetadataVerifyMixin:
    """
    Utilities for verifying sample image metadata and metadata in general against another version
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
