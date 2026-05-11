import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(scope="session")
def test_app():
    return app


@pytest.fixture
def client(test_app):
    return TestClient(test_app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Keep in-memory activity state isolated between tests."""
    original_state = copy.deepcopy(activities)

    yield

    activities.clear()
    activities.update(original_state)
