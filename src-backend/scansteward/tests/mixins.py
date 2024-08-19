import collections
from pathlib import Path

from scansteward.imageops.models import ImageMetadata


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
