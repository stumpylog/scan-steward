from http import HTTPStatus

from django.test import TestCase

from scansteward.models import Tag
from scansteward.tests.api.utils import FakerMixin
from scansteward.tests.api.utils import GenerateTagsMixin
from scansteward.tests.mixins import DirectoriesMixin


class TestApiTagRead:
    def test_get_single_tag_not_found(self):
        resp = client.get("/api/tag/1/")

        assert resp.status_code == HTTPStatus.NOT_FOUND

    def test_get_single_tag(self):
        self.generate_root_tag_objects(1)
        instance: Tag = self.roots[0]

        resp = client.get(f"/api/tag/{instance.pk}/")

        assert resp.status_code == HTTPStatus.OK
        assert resp.json()["name"] == instance.name

    def test_list_tags(self):
        count = 10
        self.generate_root_tag_objects(count)

        resp = client.get("/api/tag/")

        assert resp.status_code == HTTPStatus.OK
        assert resp.json()["count"] == count
        assert len(resp.json()["items"]) == count

    def test_tag_paginate(self):
        count = 110

        self.generate_root_tag_objects(count)

        page = 1
        resp = client.get(f"/api/tag/?page={page}")

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert data["count"] == count
        assert len(data["items"]) == 100

        page = 2
        resp = client.get(f"/api/tag/?page={page}")

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert data["count"] == count
        assert len(data["items"]) == 10

    def test_tag_tree(self):
        root_count = 3
        child_count = 2
        self.generate_root_tag_objects(root_count)
        for root in self.roots:
            self.generate_child_tag_object(child_count, root.pk)

        single_child = self.children[0]
        self.generate_child_tag_object(1, single_child.pk)

        resp = client.get("/api/tag/tree/")
        assert resp.status_code == HTTPStatus.OK

        data = resp.json()

        for root_item in data:
            assert "children" in root_item
            assert len(root_item["children"]) == child_count
            for child in root_item["children"]:
                assert "id" in child
                if child["id"] == single_child.pk:
                    assert len(child["children"]) == 1


class TestApiTagCreate(FakerMixin, DirectoriesMixin, TestCase):
    def test_create_tag_no_parent(self):
        tag_name = self.faker.country()
        resp = client.post(
            "/api/tag/",
            content_type="application/json",
            data={"name": tag_name},
        )

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert data["name"] == tag_name
        assert "id" in data
        created_id = data["id"]

        instance = Tag.objects.get(id=created_id)
        assert instance.name == tag_name
        assert instance.description is None

    def test_create_tag_with_parent(self):
        parent = Tag.objects.create(name=self.faker.country())

        tag_name = self.faker.country()

        resp = client.post(
            "/api/tag/",
            content_type="application/json",
            data={"name": tag_name, "parent_id": parent.pk},
        )

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert data["name"] == tag_name
        assert "id" in data
        assert "parent_id" in data
        assert data["parent_id"] == parent.pk
        created_id = data["id"]

        instance = Tag.objects.get(id=created_id)
        assert instance.name == tag_name
        assert instance.description is None
        assert instance.parent == parent

    def test_create_tag_exists(self):
        existing_name = self.faker.country()
        Tag.objects.create(name=existing_name)

        resp = client.post(
            "/api/tag/",
            content_type="application/json",
            data={"name": existing_name},
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST


class TestApiTagUpdate(GenerateTagsMixin, DirectoriesMixin, TestCase):
    def test_update_tag_name(self):
        self.generate_root_tag_objects(1)

        instance: Tag = self.roots[0]

        new_name = self.faker.unique.country()

        resp = client.patch(
            f"/api/tag/{instance.pk}/",
            content_type="application/json",
            data={"name": new_name},
        )

        assert resp.status_code == HTTPStatus.OK
        instance.refresh_from_db()
        assert instance.name == new_name

    def test_update_tag_parent(self):
        self.generate_root_tag_objects(2)
        root_1: Tag = self.roots[0]
        root_2: Tag = self.roots[1]
        self.generate_child_tag_object(1, root_1.pk)
        self.generate_child_tag_object(1, root_2.pk)
        child_1: Tag = self.children[0]
        child_2: Tag = self.children[1]

        assert child_1.parent is not None
        assert child_1.parent.pk == root_1.pk

        resp = client.patch(
            f"/api/tag/{child_1.pk}/",
            content_type="application/json",
            data={"parent_id": child_2.pk},
        )
        assert resp.status_code == HTTPStatus.OK

        child_1.refresh_from_db()
        assert child_1.parent is not None
        assert child_1.parent.pk == child_2.pk

    def test_update_tag_add_description(self):
        self.generate_root_tag_objects(1)
        root: Tag = self.roots[0]

        assert root.description is None

        resp = client.patch(
            f"/api/tag/{root.pk}/",
            content_type="application/json",
            data={"description": self.faker.sentence()},
        )
        assert resp.status_code == HTTPStatus.OK

        root.refresh_from_db()
        assert root.description is not None


class TestApiTagDelete(GenerateTagsMixin, DirectoriesMixin, TestCase):
    def test_delete_single_tag(self):
        self.generate_root_tag_objects(1)
        root: Tag = self.roots[0]
        resp = client.delete(
            f"/api/tag/{root.pk}/",
        )

        assert resp.status_code == HTTPStatus.NO_CONTENT

    def test_delete_single_tag_not_found(self):
        resp = client.delete(
            "/api/tag/1/",
        )

        assert resp.status_code == HTTPStatus.NOT_FOUND
