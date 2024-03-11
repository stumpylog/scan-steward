import tempfile
from collections.abc import Sequence
from contextlib import ExitStack
from os import PathLike
from pathlib import Path

from django.test import override_settings


class TemporaryDirectoryMixin:
    """
    Provides a helper which will generate new temporary directories as needed,
    which will all be removed when the class is torn down
    """

    @classmethod
    def setUpClass(cls):
        cls._dir_stack = ExitStack()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._dir_stack.close()
        super().tearDownClass()

    def get_new_temporary_dir(self) -> Path:
        """
        Generates a new temporary directory which will be cleaned up on tearDown
        """
        tmp_dir = self._dir_stack.enter_context(tempfile.TemporaryDirectory())
        return Path(tmp_dir)


class DirectoriesMixin(TemporaryDirectoryMixin):
    """
    Creates and overrides settings for all folders and paths defined, then ensures
    they are cleaned up on exit
    """

    def setUp(self) -> None:
        super().setUp()
        base_dir = self.get_new_temporary_dir()
        data = base_dir / "data"
        logs = data / "logs"
        media = base_dir / "media"
        thumbnail = media / "thumbnails"
        fullsize = media / "fullsize"
        for x in [data, logs, media, thumbnail, fullsize]:
            x.mkdir(parents=True)
        self._overrides = override_settings(
            DATA_DIR=data,
            LOGGING_DIR=logs,
            MEDIA_ROOT=media,
            THUMBNAIL_DIR=thumbnail,
            FULL_SIZE_DIR=fullsize,
        )
        self._overrides.enable()

    def tearDown(self) -> None:
        super().tearDown()
        self._overrides.disable()


class FileSystemAssertsMixin:
    """
    Utilities for checks various state information of the file system
    """

    def assertIsFile(self, path: PathLike | str):  # noqa: N802
        assert Path(path).resolve().is_file(), f"File does not exist: {path}"

    def assertIsNotFile(self, path: PathLike | str):  # noqa: N802
        assert not Path(path).resolve().is_file(), f"File does exist: {path}"

    def assertIsDir(self, path: PathLike | str):  # noqa: N802
        assert Path(path).resolve().is_dir(), f"Dir does not exist: {path}"

    def assertIsNotDir(self, path: PathLike | str):  # noqa: N802
        assert not Path(path).resolve().is_dir(), f"Dir does exist: {path}"

    def assertFilesEqual(  # noqa: N802
        self,
        path1: PathLike | str,
        path2: PathLike | str,
    ):
        path1 = Path(path1)
        path2 = Path(path2)
        import hashlib

        hash1 = hashlib.sha256(path1.read_bytes()).hexdigest()
        hash2 = hashlib.sha256(path2.read_bytes()).hexdigest()

        assert hash1 == hash2, "File SHA256 mismatch"

    def assertFileContents(self, file: PathLike | str, content: bytes | bytearray):  # noqa: N802
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
