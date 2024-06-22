from typing import TYPE_CHECKING

from faker import Faker

from scansteward.models import Tag


class FakerMixin:
    def setUp(self) -> None:
        self.faker = Faker()
        if TYPE_CHECKING:
            assert hasattr(self, "setUp")
            assert callable(self.setUp)
        return super().setUp()


class GenerateTagsMixin(FakerMixin):
    def setUp(self) -> None:
        self.roots: list[Tag] = []
        self.children: list[Tag] = []
        return super().setUp()

    def generate_root_tag_objects(self, count: int, *, with_description: bool = False) -> None:
        """
        Directly create root Tag objects into the database
        """
        Tag.objects.all().delete()
        for _ in range(count):
            name = self.faker.unique.word()
            description = self.faker.sentence if with_description else None
            self.roots.append(Tag.objects.create(name=name, description=description))

    def generate_child_tag_object(self, count: int, parent_id: int, *, with_description: bool = False):
        """
        Directly create child Tags under the given parent ID
        """
        parent = Tag.objects.get(id=parent_id)
        for _ in range(count):
            name = self.faker.unique.word()
            description = self.faker.sentence if with_description else None
            self.children.append(Tag.objects.create(name=name, description=description, parent=parent))
