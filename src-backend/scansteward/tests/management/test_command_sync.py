import shutil

from django.core.management import call_command
from django.test import TestCase

from scansteward.models import Image
from scansteward.tests.mixins import DirectoriesMixin
from scansteward.tests.mixins import SampleDirMixin
from scansteward.tests.mixins import TemporaryDirectoryMixin


class TestSyncCommand(DirectoriesMixin, SampleDirMixin, TemporaryDirectoryMixin, TestCase):
    def test_sync_command(self):
        tmp_dir = self.get_new_temporary_dir()
        _ = shutil.copy(self.SAMPLE_ONE, tmp_dir / self.SAMPLE_ONE.name)

        call_command("index", str(tmp_dir))

        img = Image.objects.first()

        assert img is not None
        assert not img.is_dirty

        img.description = "This is a new, changed, neat description"
        img.save()
        img.refresh_from_db()

        assert img.is_dirty

        call_command("sync")

        img.refresh_from_db()

        assert not img.is_dirty
