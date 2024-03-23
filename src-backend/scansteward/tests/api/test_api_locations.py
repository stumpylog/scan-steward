from http import HTTPStatus

from django.test import TestCase

from scansteward.models import Location


def util_create_location_object(
    country: str,
    subdivision: str | None = None,
    city: str | None = None,
    location: str | None = None,
) -> int:
    instance = Location.objects.create(
        country_code=country,
        subdivision_code=subdivision,
        city=city,
        sub_location=location,
    )
    return instance.pk


class TestCreateLocation(TestCase):
    def test_location_create_country_only(self):
        resp = self.client.post(
            "/api/location/",
            content_type="application/json",
            data={"country_code": "US"},
        )

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert Location.objects.count() == 1
        assert Location.objects.get(pk=data["id"]).country_code == "US"

    def test_location_create_country_and_state(self):
        resp = self.client.post(
            "/api/location/",
            content_type="application/json",
            data={"country_code": "US", "subdivision_code": "US-CA"},
        )

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert Location.objects.count() == 1
        assert Location.objects.get(pk=data["id"]).country_code == "US"
        assert Location.objects.get(pk=data["id"]).subdivision_code == "US-CA"

    def test_location_create_country_and_state_and_city(self):
        resp = self.client.post(
            "/api/location/",
            content_type="application/json",
            data={"country_code": "US", "subdivision_code": "US-CA", "city": "San Francisco"},
        )

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert Location.objects.count() == 1
        assert Location.objects.get(pk=data["id"]).country_code == "US"
        assert Location.objects.get(pk=data["id"]).subdivision_code == "US-CA"
        assert Location.objects.get(pk=data["id"]).city == "San Francisco"

    def test_location_create_country_and_state_and_city_and_sublocation(self):
        resp = self.client.post(
            "/api/location/",
            content_type="application/json",
            data={
                "country_code": "US",
                "subdivision_code": "US-CA",
                "city": "San Francisco",
                "sub_location": "Fisherman's Wharf",
            },
        )

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()
        assert Location.objects.count() == 1
        assert Location.objects.get(pk=data["id"]).country_code == "US"
        assert Location.objects.get(pk=data["id"]).subdivision_code == "US-CA"
        assert Location.objects.get(pk=data["id"]).city == "San Francisco"
        assert Location.objects.get(pk=data["id"]).sub_location == "Fisherman's Wharf"

    def test_location_create_country_and_state_invalid(self):
        resp = self.client.post(
            "/api/location/",
            content_type="application/json",
            data={"country_code": "US", "subdivision_code": "DE-HM"},
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST
        assert Location.objects.count() == 0

    def test_location_already_exists(self):
        resp = self.client.post(
            "/api/location/",
            content_type="application/json",
            data={"country_code": "US", "subdivision_code": "US-CA"},
        )
        assert resp.status_code == HTTPStatus.CREATED

        resp = self.client.post(
            "/api/location/",
            content_type="application/json",
            data={"country_code": "US", "subdivision_code": "US-CA"},
        )
        assert resp.status_code == HTTPStatus.CONFLICT


class TestReadLocation(TestCase):

    def test_read_single_location(self):
        id = util_create_location_object("US", "US-CA", "San Francisco", "Golden Gate Bridge")

        resp = self.client.get(f"/api/location/{id}/")

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert data["id"] == id
        assert data["country_code"] == "US"
        assert data["subdivision_code"] == "US-CA"
        assert data["city"] == "San Francisco"
        assert data["sub_location"] == "Golden Gate Bridge"

    def test_read_single_location_not_found(self):
        resp = self.client.get("/api/location/5/")

        assert resp.status_code == HTTPStatus.NOT_FOUND

    def test_read_all_locations(self):
        id1 = util_create_location_object("US", "US-CA", "San Francisco", "Golden Gate Bridge")
        id2 = util_create_location_object("US", "US-CA", "Los Angeles", "Grand Central Market")

        resp = self.client.get("/api/location/")

        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        assert len(data) == 2
        # Checks ordering as well
        assert data["items"][1]["id"] == id1
        assert data["items"][0]["id"] == id2


class TestUpdateLocation(TestCase):
    def test_update_city(self):
        id = util_create_location_object("US", "US-CA", "San Francisco", "Golden Gate Bridge")

        resp = self.client.patch(
            f"/api/location/{id}/",
            content_type="application/json",
            data={"city": "New York"},
        )

        assert resp.status_code == HTTPStatus.OK
        assert Location.objects.get(pk=id).city == "New York"

    def test_update_subdivision_code_with_no_country(self):
        id = util_create_location_object("US", "US-CA", "San Francisco", "Golden Gate Bridge")

        resp = self.client.patch(
            f"/api/location/{id}/",
            content_type="application/json",
            data={"subdivision_code": "US-NY"},
        )

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        data = resp.json()
        assert "Subdivision must also include country code" in data["detail"][0]["msg"]
        assert Location.objects.get(pk=id).subdivision_code == "US-CA"

    def test_update_subdivision_code_with_wrong_country(self):
        id = util_create_location_object("US", "US-CA", "San Francisco", "Golden Gate Bridge")

        resp = self.client.patch(
            f"/api/location/{id}/",
            content_type="application/json",
            data={"country_code": "US", "subdivision_code": "AM-AG"},
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST
        data = resp.json()
        from pprint import pprint

        pprint(data)
        assert "Subdivision AM-AG is not in country US" in data["detail"]
        assert Location.objects.get(pk=id).subdivision_code == "US-CA"

    def test_update_no_data(self):
        id = util_create_location_object("US", "US-CA", "San Francisco", "Golden Gate Bridge")
        resp = self.client.patch(f"/api/location/{id}/", content_type="application/json", data={})

        assert resp.status_code == HTTPStatus.BAD_REQUEST

    def test_update_country_and_subdivision(self):
        id = util_create_location_object("US", "US-CA", "San Francisco", "Golden Gate Bridge")
        resp = self.client.patch(
            f"/api/location/{id}/",
            content_type="application/json",
            data={"country_code": "FR", "subdivision_code": "FR-IDF"},
        )

        assert resp.status_code == HTTPStatus.OK
        assert Location.objects.get(pk=id).country_code == "FR"
        assert Location.objects.get(pk=id).subdivision_code == "FR-IDF"


class TestDeleteLocation(TestCase):
    def test_delete_location(self):
        id = util_create_location_object("US", "US-CA", "San Francisco", "Golden Gate Bridge")
        resp = self.client.delete(f"/api/location/{id}/")

        assert resp.status_code == HTTPStatus.NO_CONTENT
        assert Location.objects.filter(pk=id).exists() is False

    def test_delete_location_not_found(self):
        id = util_create_location_object("US", "US-CA", "San Francisco", "Golden Gate Bridge")
        resp = self.client.delete(f"/api/location/{id + 1}/")
        assert resp.status_code == HTTPStatus.NOT_FOUND
