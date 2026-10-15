"""Validation rules for FlightGraph LLM intents."""

import re

from api.assistant_models import AssistantIntent


class InvalidAssistantIntent(ValueError):
    """Raised when an LLM intent fails application validation."""


def validate_iata(value: str | None) -> str:
    """Validate and normalize a three-letter airport code."""

    if value is None:
        raise InvalidAssistantIntent("An airport code is required.")

    normalized = value.strip().upper()

    if not re.fullmatch(r"[A-Z]{3}", normalized):
        raise InvalidAssistantIntent(
            "Airport codes must contain exactly three letters."
        )

    return normalized


def validate_intent(intent: AssistantIntent) -> AssistantIntent:
    """Validate an LLM operation and its required parameters."""

    if intent.operation == "UNSUPPORTED":
        raise InvalidAssistantIntent(
            "This question is not supported by FlightGraph."
        )

    source = validate_iata(intent.source_iata)

    if intent.operation == "FIND_SHORTEST_ROUTE":
        destination = validate_iata(intent.destination_iata)

        if source == destination:
            raise InvalidAssistantIntent(
                "Source and destination airports must be different."
            )

        return AssistantIntent(
            operation=intent.operation,
            source_iata=source,
            destination_iata=destination,
        )

    if intent.destination_iata is not None:
        raise InvalidAssistantIntent(
            "This operation does not accept a destination airport."
        )

    return AssistantIntent(
        operation=intent.operation,
        source_iata=source,
        destination_iata=None,
    )
