from django.core.management import call_command
from django.test import TestCase

from scansteward.models import Image
from scansteward.tests.mixins import IndexedEnvironmentMixin


class TestSyncCommand(IndexedEnvironmentMixin, TestCase):
    def test_sync_command(self):
        img = Image.objects.get(pk=1)

        assert img is not None
        assert not img.is_dirty

        img.description = "This is a new, changed, neat description"
        img.save()
        img.refresh_from_db()

        assert img.is_dirty

        call_command("sync")

        img.refresh_from_db()

        assert not img.is_dirty
