import datetime
from http import HTTPStatus

from django.test import TestCase

from scansteward.models import RoughDate
from scansteward.tests.api.utils import GenerateRoughDateMixin
from scansteward.tests.mixins import DirectoriesMixin


class TestApiRoughDateCreate(DirectoriesMixin, TestCase):
    def setUp(self) -> None:
        self.today = datetime.datetime.now(tz=datetime.timezone.utc).date()
        return super().setUp()

    def test_create_rough_date_all_valid(self):
        resp = self.client.post(
            "/api/date/",
            content_type="application/json",
            data={
                "date": self.today.isoformat(),
                "month_valid": True,
                "day_valid": True,
            },
        )
        assert resp.status_code == HTTPStatus.CREATED

        obj = RoughDate.objects.get(id=resp.json()["id"])

        assert obj is not None
        assert obj.date == self.today
        assert obj.month_valid
        assert obj.day_valid

    def test_create_rough_date_valid_month(self):
        resp = self.client.post(
            "/api/date/",
            content_type="application/json",
            data={
                "date": self.today.isoformat(),
                "month_valid": True,
                "day_valid": False,
            },
        )
        assert resp.status_code == HTTPStatus.CREATED

        obj = RoughDate.objects.get(id=resp.json()["id"])

        assert obj is not None
        assert obj.date == self.today
        assert obj.month_valid
        assert not obj.day_valid

    def test_create_rough_date_invalid_month_valid_date(self):
        resp = self.client.post(
            "/api/date/",
            content_type="application/json",
            data={
                "date": self.today.isoformat(),
                "month_valid": False,
                "day_valid": True,
            },
        )
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        assert RoughDate.objects.count() == 0

    def test_create_date_already_exists(self):
        resp = self.client.post(
            "/api/date/",
            content_type="application/json",
            data={
                "date": self.today.isoformat(),
                "month_valid": True,
                "day_valid": False,
            },
        )
        assert resp.status_code == HTTPStatus.CREATED

        resp = self.client.post(
            "/api/date/",
            content_type="application/json",
            data={
                "date": self.today.isoformat(),
                "month_valid": True,
                "day_valid": False,
            },
        )
        assert resp.status_code == HTTPStatus.CONFLICT


class TestApiRoughDateRead(GenerateRoughDateMixin, DirectoriesMixin, TestCase):
    def generate_rough_dates(self, count: int) -> None:
        for _ in range(count):
            date = self.faker.date_this_century()
            month_valid = self.faker.pybool()
            day_valid = self.faker.pybool() if month_valid else False
            self.dates.append(
                RoughDate.objects.create(date=date, month_valid=month_valid, day_valid=day_valid),
            )

    def setUp(self) -> None:
        self.dates = []
        return super().setUp()

    def test_read_no_dates(self):
        resp = self.client.get(
            "/api/date/",
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.OK

        assert resp.json()["count"] == 0
        assert len(resp.json()["items"]) == 0

    def test_read_dates(self):
        self.generate_rough_dates(2)

        resp = self.client.get(
            "/api/date/",
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["count"] == 2
        assert len(data["items"]) == 2
        for date in self.dates:
            assert {
                "id": date.pk,
                "date": date.date.isoformat(),
                "month_valid": date.month_valid,
                "day_valid": date.day_valid,
            } in data["items"]

    def test_read_single_date(self):
        self.generate_rough_dates(1)

        date = self.dates[0]

        resp = self.client.get(
            f"/api/date/{date.pk}/",
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert {
            "id": date.pk,
            "date": date.date.isoformat(),
            "month_valid": date.month_valid,
            "day_valid": date.day_valid,
        } == data


class TestApiRoughDateUpdate(GenerateRoughDateMixin, TestCase):
    def setUp(self) -> None:
        self.today = datetime.datetime.now(tz=datetime.timezone.utc).date()
        return super().setUp()

    def test_update_rough_date_date(self):
        self.generate_rough_dates(1)

        date = self.dates[0]

        new_date = self.today + datetime.timedelta(days=1)
        resp = self.client.patch(
            f"/api/date/{date.pk}/",
            content_type="application/json",
            data={"date": new_date.isoformat()},
        )

        assert resp.status_code == HTTPStatus.OK

        date.refresh_from_db()

        assert date.date == new_date

    def test_update_rough_date_month_valid(self):
        self.generate_rough_dates(1)

        date = self.dates[0]
        date.month_valid = False
        date.day_valid = False
        date.save()

        resp = self.client.patch(
            f"/api/date/{date.pk}/",
            content_type="application/json",
            data={"month_valid": True},
        )

        assert resp.status_code == HTTPStatus.OK

        date.refresh_from_db()

        assert date.month_valid

    def test_update_rough_date_day_valid(self):
        self.generate_rough_dates(1)

        date = self.dates[0]
        date.month_valid = True
        date.day_valid = False
        date.save()

        resp = self.client.patch(
            f"/api/date/{date.pk}/",
            content_type="application/json",
            data={"day_valid": True},
        )

        assert resp.status_code == HTTPStatus.OK

        date.refresh_from_db()

        assert date.day_valid

    def test_update_rough_date_invalid_combo(self):
        self.generate_rough_dates(1)

        date = self.dates[0]
        date.month_valid = False
        date.day_valid = False
        date.save()

        resp = self.client.patch(
            f"/api/date/{date.pk}/",
            content_type="application/json",
            data={"day_valid": True},
        )

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        date.refresh_from_db()

        assert not date.day_valid

    def test_update_rough_date_empty_data(self):
        self.generate_rough_dates(1)

        date = self.dates[0]
        date.month_valid = False
        date.day_valid = False
        date.save()

        resp = self.client.patch(
            f"/api/date/{date.pk}/",
            content_type="application/json",
            data={},
        )

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


class TestApiRoughDateDelete(GenerateRoughDateMixin, DirectoriesMixin, TestCase):
    def test_delete_rough_date(self):
        self.generate_rough_dates(1)

        date = self.dates[0]

        resp = self.client.delete(f"/api/date/{date.pk}/")

        assert resp.status_code == HTTPStatus.NO_CONTENT
        assert RoughDate.objects.count() == 0

    def test_delete_rough_date_not_found(self):
        self.generate_rough_dates(1)

        date = self.dates[0]

        resp = self.client.delete(f"/api/date/{date.pk + 2}/")

        assert resp.status_code == HTTPStatus.NOT_FOUND
