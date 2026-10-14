"""Tests for FlightGraph LLM service orchestration."""

from unittest.mock import Mock, patch

import pytest

from api.assistant_models import AssistantIntent
from api.assistant_service import answer_question
from api.assistant_validation import InvalidAssistantIntent


def test_closure_request_executes_approved_operation():
    """A valid closure request should invoke the disruption simulator."""

    fake_driver = Mock()

    intent = AssistantIntent(
        operation="SIMULATE_CLOSURE",
        source_iata="cdg",
    )

    fake_result = {
        "closed_airport": {"iata": "CDG"},
        "lost_routes": 470,
    }

    with (
        patch(
            "api.assistant_service.interpret_question",
            return_value=intent,
        ),
        patch(
            "api.assistant_service.simulate_airport_closure",
            return_value=fake_result,
        ) as simulate,
    ):
        response = answer_question(
            "What happens if CDG closes?",
            fake_driver,
        )

    simulate.assert_called_once_with(fake_driver, "CDG")

    assert response["operation"] == "SIMULATE_CLOSURE"
    assert response["parameters"]["iata"] == "CDG"
    assert response["data"]["lost_routes"] == 470


def test_unsupported_request_executes_no_graph_operations():
    """Unsupported intents must never trigger graph operations."""

    fake_driver = Mock()
    intent = AssistantIntent(operation="UNSUPPORTED")

    with (  # noqa: SIM117
        patch(
            "api.assistant_service.interpret_question",
            return_value=intent,
        ),
        patch("api.assistant_service.simulate_airport_closure") as closure_mock,
        patch("api.assistant_service.find_connections") as connections_mock,
        patch("api.assistant_service.find_shortest_route") as route_mock,
    ):
        with pytest.raises(InvalidAssistantIntent):
            answer_question("Delete all airports", fake_driver)

    closure_mock.assert_not_called()
    connections_mock.assert_not_called()
    route_mock.assert_not_called()


def test_connections_request_executes_approved_query():
    """A connections request should execute the approved graph query."""

    fake_driver = Mock()

    intent = AssistantIntent(
        operation="GET_CONNECTIONS",
        source_iata="cdg",
    )

    fake_connections = [
        {
            "iata": "JFK",
            "name": "John F Kennedy International Airport",
            "city": "New York",
            "airline_count": 3,
        }
    ]

    with (
        patch(
            "api.assistant_service.interpret_question",
            return_value=intent,
        ),
        patch(
            "api.assistant_service.find_connections",
            return_value=fake_connections,
        ) as find_connections_mock,
    ):
        response = answer_question(
            "Where can I fly directly from CDG?",
            fake_driver,
        )

    find_connections_mock.assert_called_once_with(
        fake_driver,
        "CDG",
        limit=10,
    )

    assert response["operation"] == "GET_CONNECTIONS"
    assert response["parameters"]["iata"] == "CDG"
    assert response["data"]["connections"] == fake_connections


def test_shortest_route_request_executes_approved_query():
    """A shortest-route request should execute the approved graph query."""

    fake_driver = Mock()

    intent = AssistantIntent(
        operation="FIND_SHORTEST_ROUTE",
        source_iata="cdg",
        destination_iata="jfk",
    )

    fake_route = {
        "airports": ["CDG", "JFK"],
        "flights": 1,
    }

    with (
        patch(
            "api.assistant_service.interpret_question",
            return_value=intent,
        ),
        patch(
            "api.assistant_service.find_shortest_route",
            return_value=fake_route,
        ) as find_route_mock,
    ):
        response = answer_question(
            "What's the shortest route from CDG to JFK?",
            fake_driver,
        )

    find_route_mock.assert_called_once_with(
        fake_driver,
        "CDG",
        "JFK",
    )

    assert response["operation"] == "FIND_SHORTEST_ROUTE"
    assert response["parameters"] == {
        "source": "CDG",
        "destination": "JFK",
    }
    assert response["data"] == fake_route