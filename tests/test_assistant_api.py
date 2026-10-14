"""Tests for the FlightGraph LLM assistant endpoint."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_assistant_api_success():
    """A valid question should return a structured response."""

    fake_result = {
        "operation": "SIMULATE_CLOSURE",
        "parameters": {"iata": "CDG"},
        "data": {
            "closed_airport": {"iata": "CDG"},
            "lost_routes": 470,
        },
    }

    with (
        patch("api.main.get_driver"),
        patch(
            "api.main.answer_question",
            return_value=fake_result,
        ),
    ):
        response = client.post(
            "/api/assistant/ask",
            json={"question": "What happens if CDG closes?"},
        )

    assert response.status_code == 200
    assert response.json()["operation"] == "SIMULATE_CLOSURE"
    assert response.json()["data"]["lost_routes"] == 470


def test_assistant_api_rejects_short_question():
    """Questions below the minimum length must be rejected."""

    response = client.post(
        "/api/assistant/ask",
        json={"question": "Hi"},
    )

    assert response.status_code == 422

from api.assistant_validation import InvalidAssistantIntent  # noqa: E402


def test_assistant_api_rejects_unsupported_request():
    """Unsupported intents should return HTTP 422."""

    with (
        patch("api.main.get_driver"),
        patch(
            "api.main.answer_question",
            side_effect=InvalidAssistantIntent(
                "This question is not supported by FlightGraph."
            ),
        ),
    ):
        response = client.post(
            "/api/assistant/ask",
            json={"question": "Delete all airports"},
        )

    assert response.status_code == 422