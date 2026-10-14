"""Pydantic models for the FlightGraph LLM assistant."""

from typing import Literal

from pydantic import BaseModel, Field


class AssistantIntent(BaseModel):
    """Represent a validated intent extracted by the LLM."""

    operation: Literal[
        "GET_CONNECTIONS",
        "FIND_SHORTEST_ROUTE",
        "SIMULATE_CLOSURE",
        "UNSUPPORTED",
    ]

    source_iata: str | None = Field(
        default=None,
        description="IATA code of the source airport.",
    )

    destination_iata: str | None = Field(
        default=None,
        description="IATA code of the destination airport.",
    )


class AssistantQuestion(BaseModel):
    """Natural-language question submitted to the LLM assistant."""

    question: str = Field(
        min_length=3,
        max_length=500,
        description="Question about the FlightGraph airline network.",
    )


class AssistantResponse(BaseModel):
    """Structured response from an approved assistant operation."""

    operation: str
    parameters: dict[str, str]
    data: dict