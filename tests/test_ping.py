from fastapi.testclient import TestClient
from fastapi_ipykernel_sandbox.main import app
import pytest

@pytest.fixture
def client():
    return TestClient(app)


def test_ping(client):
    assert client.get("/ping").status_code == 204
