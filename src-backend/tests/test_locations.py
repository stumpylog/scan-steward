from faker import Faker
from litestar import status_codes
from litestar.testing import AsyncTestClient


class TestLocationController:
    async def test_get_no_locations(self, test_client: AsyncTestClient):
        response = await test_client.get("/api/v1/location")
        assert response.status_code == status_codes.HTTP_200_OK
        assert len(response.json()["items"]) == 0

    async def test_create_and_get_location(self, test_client: AsyncTestClient):
        data = {"name": "A Test Location"}
        response = await test_client.post("/api/v1/location", json=data)
        assert response.status_code == status_codes.HTTP_201_CREATED

        resp_data = response.json()
        assert resp_data["id"] == 1
        assert resp_data["name"] == "A Test Location"

        response = await test_client.get("/api/v1/location")
        assert response.status_code == status_codes.HTTP_200_OK

        resp_data = response.json()
        assert len(resp_data["items"]) == 1

    async def test_create_and_update_location(self, test_client: AsyncTestClient):
        data = {"name": "A Test Location"}
        response = await test_client.post("/api/v1/location", json=data)
        assert response.status_code == status_codes.HTTP_201_CREATED

        resp_data = response.json()
        assert resp_data["id"] == 1
        assert resp_data["name"] == "A Test Location"
        location_id = resp_data["id"]

        data = {"name": "A New Name"}
        response = await test_client.put(f"/api/v1/location/{location_id}", json=data)
        assert response.status_code == status_codes.HTTP_200_OK

        resp_data = response.json()
        assert resp_data["id"] == 1
        assert resp_data["name"] == "A New Name"

    async def test_get_single_location(self, test_client: AsyncTestClient):
        response = await test_client.post("/api/v1/location", json={"name": "A Test Location"})
        assert response.status_code == status_codes.HTTP_201_CREATED

        resp_data = response.json()
        assert resp_data["id"] == 1
        assert resp_data["name"] == "A Test Location"
        location_id = resp_data["id"]

        response = await test_client.get(f"/api/v1/location/{location_id}")
        assert response.status_code == status_codes.HTTP_200_OK

        resp_data = response.json()
        assert resp_data["id"] == 1
        assert resp_data["name"] == "A Test Location"

    async def test_get_location_not_found(self, test_client: AsyncTestClient):
        response = await test_client.get("/api/v1/location/1")
        assert response.status_code == status_codes.HTTP_404_NOT_FOUND

    async def test_update_location_not_found(self, test_client: AsyncTestClient):
        response = await test_client.put("/api/v1/location/1", json={"name": "A New Name"})
        assert response.status_code == status_codes.HTTP_404_NOT_FOUND

    async def test_pagination(self, test_client: AsyncTestClient, faker: Faker):
        for _ in range(15):
            data = {"name": faker.city()}
            response = await test_client.post("/api/v1/location", json=data)
            assert response.status_code == status_codes.HTTP_201_CREATED

        response = await test_client.get("/api/v1/location")
        assert response.status_code == status_codes.HTTP_200_OK

        resp_data = response.json()
        assert resp_data["limit"] == 10
        assert resp_data["offset"] == 0
        assert resp_data["total"] == 15
        assert len(resp_data["items"]) == 10

        response = await test_client.get("/api/v1/location?offset=1&limit=5")
        assert response.status_code == status_codes.HTTP_200_OK
        resp_data = response.json()
        assert resp_data["limit"] == 5
        assert resp_data["offset"] == 0
        assert resp_data["total"] == 15
        assert len(resp_data["items"]) == 5
