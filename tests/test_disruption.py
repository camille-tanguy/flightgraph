"""Tests for the FlightGraph disruption API."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from api.disruption import ensure_baseline_graph, simulate_airport_closure
from api.main import app

client = TestClient(app)


# --------------------------------------------------
# 1. Test invalid IATA codes
# --------------------------------------------------


def test_disruption_invalid_iata():
    """Reject invalid airport codes."""

    response = client.get("/api/disruptions/airports/1234")

    assert response.status_code == 422


# --------------------------------------------------
# 2. Test unknown airports
# --------------------------------------------------


def test_disruption_airport_not_found():
    """Return HTTP 404 when an airport does not exist."""

    with (
        patch("api.main.get_driver"),
        patch(
            "api.main.simulate_airport_closure",
            side_effect=ValueError("Airport 'ZZZ' not found."),
        ),
    ):
        response = client.get("/api/disruptions/airports/ZZZ")

    assert response.status_code == 404
    assert response.json()["detail"] == "Airport 'ZZZ' not found."


# --------------------------------------------------
# 3. Test ambiguous IATA codes
# --------------------------------------------------


def test_disruption_ambiguous_iata():
    """Return HTTP 409 when multiple airports share an IATA code."""

    with (
        patch("api.main.get_driver"),
        patch(
            "api.main.simulate_airport_closure",
            side_effect=ValueError("Airport code 'ABC' is ambiguous."),
        ),
    ):
        response = client.get("/api/disruptions/airports/ABC")

    assert response.status_code == 409
    assert "ambiguous" in response.json()["detail"]


# --------------------------------------------------
# 4. Test successful airport closure
# --------------------------------------------------


def test_disruption_success():
    """Return structured results for a successful airport closure."""

    mock_result = {
        "closed_airport": {
            "airport_id": 1382,
            "name": "Charles de Gaulle International Airport",
            "iata": "CDG",
        },
        "lost_routes": 470,
        "baseline": {
            "total_components": 4491,
            "largest_component": 3188,
            "total_airports": 7698,
            "isolated_airports": 4484,
        },
        "disrupted": {
            "total_components": 4492,
            "largest_component": 3186,
            "total_airports": 7697,
            "isolated_airports": 4485,
        },
        "changes": {
            "components": 1,
            "largest_component": -2,
            "isolated_airports": 1,
        },
    }

    with (
        patch("api.main.get_driver"),
        patch(
            "api.main.simulate_airport_closure",
            return_value=mock_result,
        ),
    ):
        response = client.get("/api/disruptions/airports/CDG")

    assert response.status_code == 200
    assert response.json() == mock_result


# --------------------------------------------------
# 5. Test cleanup after simulation failure
# --------------------------------------------------


def test_simulation_cleanup_after_failure():
    """Attempt to remove the temporary graph when WCC fails."""

    driver = MagicMock()

    airport = {
        "airport_id": 1382,
        "name": "Charles de Gaulle International Airport",
        "iata": "CDG",
    }

    baseline = {
        "total_components": 4491,
        "largest_component": 3188,
        "total_airports": 7698,
        "isolated_airports": 4484,
    }

    # Simulate successful airport identification and graph creation,
    # followed by a failure during the disrupted WCC calculation.
    with (
        patch(
            "api.disruption.find_airport",
            return_value=airport,
        ),
        patch(
            "api.disruption.get_connectivity_metrics",
            side_effect=[
                baseline,
                RuntimeError("WCC failed"),
            ],
        ),
        patch(
            "api.disruption.get_graph_relationship_count",
            return_value=36906,
        ),
        patch(
            "api.disruption.create_disruption_graph",
            return_value={"route_count": 36436},
        ),
        pytest.raises(RuntimeError, match="WCC failed"),
    ):
        simulate_airport_closure(driver, "CDG")

    # Verify that the simulator attempted to clean up
    # its temporary GDS graph, despite the WCC failure.
    session = driver.session.return_value.__enter__.return_value

    assert any("gds.graph.drop" in call.args[0] for call in session.run.call_args_list)


# --------------------------------------------------
# 6. Regression tests
# --------------------------------------------------


def test_existing_baseline_graph_is_reused() -> None:
    """Do not recreate the baseline graph when it already exists."""

    driver = MagicMock()
    session = driver.session.return_value.__enter__.return_value
    session.run.return_value.single.return_value = {"exists": True}

    ensure_baseline_graph(driver)

    assert session.run.call_count == 1
    assert "gds.graph.exists" in session.run.call_args.args[0]


def test_missing_baseline_graph_is_created() -> None:
    """Create the baseline graph when it is missing."""

    driver = MagicMock()
    session = driver.session.return_value.__enter__.return_value
    session.run.return_value.single.return_value = {"exists": False}

    ensure_baseline_graph(driver)

    assert session.run.call_count == 2

    projection_query = session.run.call_args.args[0]

    assert "gds.graph.project" in projection_query
    assert "FLIES_TO" in projection_query
