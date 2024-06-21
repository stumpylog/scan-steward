from http import HTTPStatus

from django.test.client import Client


class TestCustom404:
    def test_custom_404_handle(self, client: Client):
        resp = client.get("/api/thisisnthere/")

        assert resp.status_code == HTTPStatus.NOT_FOUND

        data = resp.json()

        assert data["error"] == 'The resource "/api/thisisnthere/" was not found'
        assert data["status_code"] == HTTPStatus.NOT_FOUND
