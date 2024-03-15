from http import HTTPStatus

from django.test import TestCase

from scansteward.tests.mixins import DirectoriesMixin


class TestCustom404(DirectoriesMixin, TestCase):
    def test_custom_404_handle(self):
        resp = self.client.get("/api/thisisnthere/")

        assert resp.status_code == HTTPStatus.NOT_FOUND

        data = resp.json()

        assert data["error"] == 'The resource "/api/thisisnthere/" was not found'
        assert data["status_code"] == HTTPStatus.NOT_FOUND
