import random

import pytest


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return 0


@pytest.fixture(scope="session", autouse=True)
def _seed_random():
    random.seed(0)
