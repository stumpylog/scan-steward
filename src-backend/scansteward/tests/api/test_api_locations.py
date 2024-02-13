from http import HTTPStatus

from scansteward.models import Location
from scansteward.tests.api.utils import FakerTestCase


class GenerateLocationsTestCase(FakerTestCase):
    def setUp(self) -> None:
        self.roots = []
        self.children = []
        return super().setUp()

    def generate_root_locations(self, count: int, *, with_description: bool = False) -> None:
        Location.objects.all().delete()
        for _ in range(count):
            name = self.faker.unique.country()
            description = self.faker.sentence if with_description else None
            self.roots.append(Location.objects.create(name=name, description=description))

    def generate_child_locations(self, count: int, parent_id: int, *, with_description: bool = False):
        parent = Location.objects.get(id=parent_id)
        for _ in range(count):
            name = self.faker.unique.city()
            description = self.faker.sentence if with_description else None
            self.children.append(Location.objects.create(name=name, description=description, parent=parent))


class TestApiLocationRead(GenerateLocationsTestCase):
    def test_get_single_location_not_found(self):
        resp = self.client.get("/api/location/1")

        assert resp.status_code == HTTPStatus.NOT_FOUND

    def test_get_single_location(self):
        self.generate_root_locations(1)
        instance: Location = self.roots[0]

        resp = self.client.get(f"/api/location/{instance.pk}")

        assert resp.status_code == HTTPStatus.OK
        assert resp.json()["name"] == instance.name

    def test_list_locations(self):
        count = 10
        self.generate_root_locations(count)

        resp = self.client.get("/api/location/")

        assert resp.status_code == HTTPStatus.OK
        assert resp.json()["count"] == count
        assert len(resp.json()["items"]) == count

    def test_location_tree(self):
        root_count = 3
        child_count = 2
        self.generate_root_locations(root_count)
        for root in self.roots:
            self.generate_child_locations(child_count, root.pk)

        single_child = self.children[0]
        self.generate_child_locations(1, single_child.pk)

        resp = self.client.get("/api/location/tree/")
        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        for root_item in data:
            assert "children" in root_item
            assert len(root_item["children"]) == child_count
            for child in root_item["children"]:
                assert "id" in child
                if child["id"] == single_child.pk:
                    assert len(child["children"]) == 1


class TestApiLocationCreate(FakerTestCase):

    def test_create_location_no_parent(self):
        location_name = self.faker.country()
        resp = self.client.post(
            "/api/location/",
            headers={"accept": "application/json"},
            content_type="application/json",
            data={"name": location_name},
        )

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert data["name"] == location_name
        assert "id" in data
        created_id = data["id"]

        instance = Location.objects.get(id=created_id)
        assert instance.name == location_name
        assert instance.description is None

    def test_create_location_with_parent(self):
        parent = Location.objects.create(name=self.faker.country())

        location_name = self.faker.country()

        resp = self.client.post(
            "/api/location/",
            headers={"accept": "application/json"},
            content_type="application/json",
            data={"name": location_name, "parent_id": parent.pk},
        )

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert data["name"] == location_name
        assert "id" in data
        assert "parent_id" in data
        assert data["parent_id"] == parent.pk
        created_id = data["id"]

        instance = Location.objects.get(id=created_id)
        assert instance.name == location_name
        assert instance.description is None
        assert instance.parent == parent

    def test_create_location_exists(self):
        existing_name = self.faker.country()
        Location.objects.create(name=existing_name)

        resp = self.client.post(
            "/api/location/",
            headers={"accept": "application/json"},
            content_type="application/json",
            data={"name": existing_name},
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST


class TestApiLocationUpdate(GenerateLocationsTestCase):
    def test_update_location_name(self):
        self.generate_root_locations(1)

        instance: Location = self.roots[0]

        new_name = self.faker.unique.country()

        resp = self.client.patch(
            f"/api/location/{instance.pk}",
            headers={"accept": "application/json"},
            content_type="application/json",
            data={"name": new_name},
        )

        assert resp.status_code == HTTPStatus.OK
        instance.refresh_from_db()
        assert instance.name == new_name

    def test_update_location_parent(self):
        self.generate_root_locations(2)
        root_1: Location = self.roots[0]
        root_2: Location = self.roots[1]
        self.generate_child_locations(1, root_1.pk)
        self.generate_child_locations(1, root_2.pk)
        child_1: Location = self.children[0]
        child_2: Location = self.children[1]

        assert child_1.parent is not None
        assert child_1.parent.pk == root_1.pk

        resp = self.client.patch(
            f"/api/location/{child_1.pk}",
            headers={"accept": "application/json"},
            content_type="application/json",
            data={"parent_id": child_2.pk},
        )
        assert resp.status_code == HTTPStatus.OK

        child_1.refresh_from_db()
        assert child_1.parent is not None
        assert child_1.parent.pk == child_2.pk

    def test_update_location_add_description(self):
        self.generate_root_locations(1)
        root: Location = self.roots[0]

        assert root.description is None

        resp = self.client.patch(
            f"/api/location/{root.pk}",
            headers={"accept": "application/json"},
            content_type="application/json",
            data={"description": self.faker.sentence()},
        )
        assert resp.status_code == HTTPStatus.OK

        root.refresh_from_db()
        assert root.description is not None


class TestApiLocationDelete(GenerateLocationsTestCase):
    def test_delete_single_location(self):
        self.generate_root_locations(1)
        root: Location = self.roots[0]
        resp = self.client.delete(f"/api/location/{root.pk}", headers={"accept": "application/json"})

        assert resp.status_code == HTTPStatus.NO_CONTENT

    def test_delete_single_location_not_found(self):
        resp = self.client.delete("/api/location/1", headers={"accept": "application/json"})

        assert resp.status_code == HTTPStatus.NOT_FOUND
