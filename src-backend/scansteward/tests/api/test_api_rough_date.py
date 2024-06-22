import datetime
from http import HTTPStatus

import pytest
from django.test.client import Client

from scansteward.models import RoughDate


@pytest.mark.django_db()
class TestApiRoughDateCreate:
    def test_create_rough_date_all_valid(self, client: Client, today: datetime.date):
        resp = client.post(
            "/api/date/",
            content_type="application/json",
            data={
                "date": today.isoformat(),
                "month_valid": True,
                "day_valid": True,
            },
        )
        assert resp.status_code == HTTPStatus.CREATED

        obj = RoughDate.objects.get(id=resp.json()["id"])

        assert obj is not None
        assert obj.date == today
        assert obj.month_valid
        assert obj.day_valid

    def test_create_rough_date_valid_month(self, client: Client, today: datetime.date):
        resp = client.post(
            "/api/date/",
            content_type="application/json",
            data={
                "date": today.isoformat(),
                "month_valid": True,
                "day_valid": False,
            },
        )
        assert resp.status_code == HTTPStatus.CREATED

        obj = RoughDate.objects.get(id=resp.json()["id"])

        assert obj is not None
        assert obj.date == today
        assert obj.month_valid
        assert not obj.day_valid

    def test_create_rough_date_invalid_month_valid_date(self, client: Client, today: datetime.date):
        resp = client.post(
            "/api/date/",
            content_type="application/json",
            data={
                "date": today.isoformat(),
                "month_valid": False,
                "day_valid": True,
            },
        )
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        assert RoughDate.objects.count() == 0

    def test_create_date_already_exists(self, client: Client, today: datetime.date):
        resp = client.post(
            "/api/date/",
            content_type="application/json",
            data={
                "date": today.isoformat(),
                "month_valid": True,
                "day_valid": False,
            },
        )
        assert resp.status_code == HTTPStatus.CREATED

        resp = client.post(
            "/api/date/",
            content_type="application/json",
            data={
                "date": today.isoformat(),
                "month_valid": True,
                "day_valid": False,
            },
        )
        assert resp.status_code == HTTPStatus.CONFLICT


@pytest.mark.django_db()
class TestApiRoughDateRead:
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

    def test_read_no_dates(self, client: Client, today: datetime.date):
        resp = client.get(
            "/api/date/",
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.OK

        assert resp.json()["count"] == 0
        assert len(resp.json()["items"]) == 0

    def test_read_dates(self, client: Client, today: datetime.date):
        self.generate_rough_dates(2)

        resp = client.get(
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

    def test_read_single_date(self, client: Client, today: datetime.date):
        self.generate_rough_dates(1)

        date = self.dates[0]

        resp = client.get(
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


@pytest.mark.django_db()
class TestApiRoughDateUpdate:
    def test_update_rough_date_date(self, client: Client, today: datetime.date):
        self.generate_rough_dates(1)

        date = self.dates[0]

        new_date = today + datetime.timedelta(days=1)
        resp = client.patch(
            f"/api/date/{date.pk}/",
            content_type="application/json",
            data={"date": new_date.isoformat()},
        )

        assert resp.status_code == HTTPStatus.OK

        date.refresh_from_db()

        assert date.date == new_date

    def test_update_rough_date_month_valid(self, client: Client, today: datetime.date):
        self.generate_rough_dates(1)

        date = self.dates[0]
        date.month_valid = False
        date.day_valid = False
        date.save()

        resp = client.patch(
            f"/api/date/{date.pk}/",
            content_type="application/json",
            data={"month_valid": True},
        )

        assert resp.status_code == HTTPStatus.OK

        date.refresh_from_db()

        assert date.month_valid

    def test_update_rough_date_day_valid(self, client: Client, today: datetime.date):
        self.generate_rough_dates(1)

        date = self.dates[0]
        date.month_valid = True
        date.day_valid = False
        date.save()

        resp = client.patch(
            f"/api/date/{date.pk}/",
            content_type="application/json",
            data={"day_valid": True},
        )

        assert resp.status_code == HTTPStatus.OK

        date.refresh_from_db()

        assert date.day_valid

    def test_update_rough_date_invalid_combo(self, client: Client, today: datetime.date):
        self.generate_rough_dates(1)

        date = self.dates[0]
        date.month_valid = False
        date.day_valid = False
        date.save()

        resp = client.patch(
            f"/api/date/{date.pk}/",
            content_type="application/json",
            data={"day_valid": True},
        )

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        date.refresh_from_db()

        assert not date.day_valid

    def test_update_rough_date_empty_data(self, client: Client, today: datetime.date):
        self.generate_rough_dates(1)

        date = self.dates[0]
        date.month_valid = False
        date.day_valid = False
        date.save()

        resp = client.patch(
            f"/api/date/{date.pk}/",
            content_type="application/json",
            data={},
        )

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.django_db()
class TestApiRoughDateDelete:
    def test_delete_rough_date(self, client: Client, today: datetime.date):
        self.generate_rough_dates(1)

        date = self.dates[0]

        resp = client.delete(f"/api/date/{date.pk}/")

        assert resp.status_code == HTTPStatus.NO_CONTENT
        assert RoughDate.objects.count() == 0

    def test_delete_rough_date_not_found(self, client: Client, today: datetime.date):
        self.generate_rough_dates(1)

        date = self.dates[0]

        resp = client.delete(f"/api/date/{date.pk + 2}/")

        assert resp.status_code == HTTPStatus.NOT_FOUND
