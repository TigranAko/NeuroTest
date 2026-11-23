import pytest
from main import app as fastapi_app


@pytest.fixture
def app():
    yield fastapi_app
    fastapi_app.dependency_overrides.clear()
