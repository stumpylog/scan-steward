from django.test import TestCase
from faker import Faker

from scansteward.models import Tag


class FakerTestCase(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        return super().setUp()


class GenerateTagsTestCase(FakerTestCase):
    def setUp(self) -> None:
        self.roots = []
        self.children = []
        return super().setUp()

    def generate_root_tags(self, count: int, *, with_description: bool = False) -> None:
        Tag.objects.all().delete()
        for _ in range(count):
            name = self.faker.unique.word()
            description = self.faker.sentence if with_description else None
            self.roots.append(Tag.objects.create(name=name, description=description))

    def generate_child_tags(self, count: int, parent_id: int, *, with_description: bool = False):
        parent = Tag.objects.get(id=parent_id)
        for _ in range(count):
            name = self.faker.unique.word()
            description = self.faker.sentence if with_description else None
            self.children.append(Tag.objects.create(name=name, description=description, parent=parent))
