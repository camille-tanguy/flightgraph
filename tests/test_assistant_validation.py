"""Tests for FlightGraph LLM intent validation."""

import pytest

from api.assistant_models import AssistantIntent
from api.assistant_validation import (
    InvalidAssistantIntent,
    validate_intent,
)


def test_valid_disruption_intent():
    """Valid closure requests should be accepted."""

    intent = AssistantIntent(
        operation="SIMULATE_CLOSURE",
        source_iata="cdg",
    )

    validated = validate_intent(intent)

    assert validated.operation == "SIMULATE_CLOSURE"
    assert validated.source_iata == "CDG"


def test_valid_shortest_route_intent():
    """Shortest-route requests require two airports."""

    intent = AssistantIntent(
        operation="FIND_SHORTEST_ROUTE",
        source_iata="CDG",
        destination_iata="JFK",
    )

    validated = validate_intent(intent)

    assert validated.destination_iata == "JFK"


def test_missing_airport_rejected():
    """Missing airport parameters must be rejected."""

    intent = AssistantIntent(
        operation="SIMULATE_CLOSURE",
    )

    with pytest.raises(InvalidAssistantIntent):
        validate_intent(intent)


def test_invalid_airport_rejected():
    """Malformed airport codes must be rejected."""

    intent = AssistantIntent(
        operation="GET_CONNECTIONS",
        source_iata="123",
    )

    with pytest.raises(InvalidAssistantIntent):
        validate_intent(intent)


def test_unsupported_operation_rejected():
    """Unsupported requests must never reach the database."""

    intent = AssistantIntent(
        operation="UNSUPPORTED",
    )

    with pytest.raises(InvalidAssistantIntent):
        validate_intent(intent)


def test_identical_airports_rejected():
    """Shortest-route requests must use different airports."""

    intent = AssistantIntent(
        operation="FIND_SHORTEST_ROUTE",
        source_iata="CDG",
        destination_iata="CDG",
    )

    with pytest.raises(InvalidAssistantIntent):
        validate_intent(intent)


def test_unexpected_destination_rejected():
    """Single-airport operations must reject extra parameters."""

    intent = AssistantIntent(
        operation="SIMULATE_CLOSURE",
        source_iata="CDG",
        destination_iata="JFK",
    )

    with pytest.raises(InvalidAssistantIntent):
        validate_intent(intent)