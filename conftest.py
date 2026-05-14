import os
import pytest

# Set the test API key before any test runs
os.environ["API_KEY"] = "test-secret-key"

from app.main import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client