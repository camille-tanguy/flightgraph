"""Tests for the FlightGraph API."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_check():
    """Verify that the health endpoint returns a successful response."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}



def test_invalid_airport_code():
    """Reject airport codes that do not contain exactly three letters."""
    response = client.get("/api/airports/AB12")

    assert response.status_code == 422


def test_invalid_connection_limit():
    """Reject requests exceeding the maximum connection limit."""
    response = client.get(
        "/api/airports/CDG/connections",
        params={"limit": 500},
    )

    assert response.status_code == 422

def test_get_airport_success():
    """Return airport information from a mocked Neo4j result."""

    airport = {
        "airport_id": 1382,
        "name": "Charles de Gaulle International Airport",
        "city": "Paris",
        "country": "France",
        "iata": "CDG",
    }

    mock_driver = MagicMock()
    mock_driver.__enter__.return_value.session.return_value.__enter__.return_value.run.return_value.single.return_value = airport

    with patch("api.main.get_driver", return_value=mock_driver):
        response = client.get("/api/airports/CDG")

    assert response.status_code == 200
    assert response.json() == airport


def test_get_airport_not_found():
    """Return HTTP 404 when an airport does not exist."""

    mock_driver = MagicMock()
    mock_driver.__enter__.return_value.session.return_value.__enter__.return_value.run.return_value.single.return_value = None

    with patch("api.main.get_driver", return_value=mock_driver):
        response = client.get("/api/airports/ZZZ")

    assert response.status_code == 404
    assert response.json()["detail"] == "Airport 'ZZZ' not found."