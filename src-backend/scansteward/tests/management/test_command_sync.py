from django.core.management import call_command
from django.test import TestCase

from scansteward.models import Image
from scansteward.models import RoughDate
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

    def test_sync_less_location(self) -> None:
        for subdivision, city, sublocation in [
            ("US-DC", "Washington D.C.", "White House"),
            ("US-WA", None, None),
            (None, None, None),
        ]:
            with self.subTest(value=f"{subdivision} {city} {sublocation}"):
                img = Image.objects.get(pk=1)

                assert img is not None
                assert not img.is_dirty

                old_location = img.location

                assert old_location is not None
                old_location.subdivision_code = subdivision
                old_location.city = city
                old_location.sub_location = sublocation
                old_location.save()

                img.refresh_from_db()

                assert img.is_dirty

                call_command("sync")

                img.refresh_from_db()

                assert not img.is_dirty

    def test_sync_less_date(self) -> None:
        for month_valid, day_valid in [(True, True), (True, False), (False, False)]:
            with self.subTest(value=f"{month_valid} {day_valid}"):
                img = Image.objects.get(pk=2)

                assert img is not None
                assert not img.is_dirty

                old_date = RoughDate.objects.get(pk=1)

                assert old_date is not None
                old_date.month_valid = month_valid
                old_date.day_valid = day_valid
                old_date.save()
                img.date = old_date
                img.save()

                img.refresh_from_db()

                assert img.is_dirty

                call_command("sync")

                img.refresh_from_db()

                assert not img.is_dirty
