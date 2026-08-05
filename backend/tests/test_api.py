from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_public_contracts_are_available() -> None:
    for path in ["/portfolio", "/funds", "/holdings", "/overlap", "/forecast", "/risk"]:
        assert client.get(path).status_code == 200
