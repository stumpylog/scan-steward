from django.test import TestCase
from faker import Faker


class FakerTestCase(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        return super().setUp()
