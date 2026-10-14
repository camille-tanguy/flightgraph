"""FlightGraph REST API.

Receive HTTP requests, validate parameters, and return structured responses.
"""

from fastapi import FastAPI, HTTPException, Path, Query
from openai import APIConnectionError, AuthenticationError, RateLimitError

from api.assistant_models import AssistantQuestion, AssistantResponse
from api.assistant_service import answer_question
from api.assistant_validation import InvalidAssistantIntent
from api.database import get_driver
from api.disruption import simulate_airport_closure
from api.graph_queries import find_connections, find_shortest_route
from api.models import (
    AirportResponse,
    ConnectionResponse,
    DisruptionResponse,
    ReachableAirportResponse,
    ShortestPathResponse,
)

# --------------------------------------------------
# 1. FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="FlightGraph API",
    description="Airline Network Resilience & Disruption Simulator",
    version="0.1.0",
)


# --------------------------------------------------
# 2. Health check
# --------------------------------------------------

@app.get("/health")
def health_check() -> dict[str, str]:
    """Check whether the API is running."""
    return {"status": "ok"}


# --------------------------------------------------
# 3. Retrieve airport information
# --------------------------------------------------

@app.get(
    "/api/airports/{iata}",
    response_model=AirportResponse,
)
def get_airport(
    iata: str = Path(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]{3}$",
        description="Three-letter IATA airport code",
    ),
) -> AirportResponse:
    """Retrieve airport information using its IATA code."""

    cypher = """
    MATCH (a:Airport {iata: $iata})
    RETURN
        a.airport_id AS airport_id,
        a.name AS name,
        a.city AS city,
        a.country AS country,
        a.iata AS iata
    LIMIT 1
    """

    with get_driver() as driver, driver.session() as session:
        result = session.run(
            cypher,
            iata=iata.upper(),
        ).single()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Airport '{iata}' not found.",
        )

    return AirportResponse.model_validate(dict(result))


# --------------------------------------------------
# 4. Retrieve direct flight connections
# --------------------------------------------------

@app.get(
    "/api/airports/{iata}/connections",
    response_model=list[ConnectionResponse],
)
def get_connections(
    iata: str = Path(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]{3}$",
        description="Three-letter IATA airport code",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of destinations",
    ),
) -> list[ConnectionResponse]:
    """Retrieve direct outgoing connections from an airport."""

    with get_driver() as driver:
        try:
            connections = find_connections(
                driver,
                iata,
                limit=limit,
            )
        except LookupError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error),
            ) from error

    return [
        ConnectionResponse.model_validate(connection)
        for connection in connections
    ]


# --------------------------------------------------
# 5. Find a shortest flight path
# --------------------------------------------------

@app.get(
    "/api/routes/shortest",
    response_model=ShortestPathResponse,
)
def get_shortest_path(
    source: str = Query(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]{3}$",
        description="Departure airport IATA code",
    ),
    destination: str = Query(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]{3}$",
        description="Arrival airport IATA code",
    ),
) -> ShortestPathResponse:
    """Find a directed shortest path between two airports."""

    with get_driver() as driver:
        result = find_shortest_route(
            driver,
            source,
            destination,
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No route found between these airports.",
        )

    return ShortestPathResponse.model_validate(result)


# --------------------------------------------------
# 6. Find reachable airports
# --------------------------------------------------

@app.get(
    "/api/airports/{iata}/reachable",
    response_model=list[ReachableAirportResponse],
)
def get_reachable_airports(
    iata: str = Path(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]{3}$",
        description="Departure airport IATA code",
    ),
    max_hops: int = Query(
        default=2,
        ge=1,
        le=3,
        description="Maximum number of flight connections",
    ),
) -> list[ReachableAirportResponse]:
    """Find airports reachable within a maximum number of flights."""

    # Cypher relationship bounds cannot be passed directly
    # as regular parameters in this pattern syntax.
    # Select one of three predefined, safe queries.
    hop_patterns = {
        1: "1..1",
        2: "1..2",
        3: "1..3",
    }

    hop_pattern = hop_patterns[max_hops]

    cypher = f"""
    MATCH (source:Airport {{iata: $iata}})
    MATCH path = (source)-[:FLIES_TO*{hop_pattern}]->(destination:Airport)
    WHERE destination <> source
    WITH destination, min(length(path)) AS hops
    RETURN
        destination.iata AS iata,
        destination.name AS name,
        hops
    ORDER BY hops ASC, iata ASC
    LIMIT 20
    """

    with get_driver() as driver, driver.session() as session:

        # Check that the departure airport exists.
        airport_exists = session.run(
            """
            MATCH (a:Airport {iata: $iata})
            RETURN count(a) > 0 AS exists
            """,
            iata=iata.upper(),
        ).single()["exists"]

        if not airport_exists:
            raise HTTPException(
                status_code=404,
                detail=f"Airport '{iata}' not found.",
            )

        # Retrieve reachable destinations.
        results = session.run(
            cypher,
            iata=iata.upper(),
        )

        airports = [
            ReachableAirportResponse.model_validate(dict(record))
            for record in results
        ]

    return airports


# --------------------------------------------------
# 7. Simulate airport disruption
# --------------------------------------------------

@app.get(
    "/api/disruptions/airports/{iata}",
    response_model=DisruptionResponse,
)
def get_airport_disruption(
    iata: str = Path(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]{3}$",
        description="IATA code of the airport to close",
    ),
) -> DisruptionResponse:
    """Simulate the closure of an airport."""

    with get_driver() as driver:
        try:
            result = simulate_airport_closure(driver, iata)
        except ValueError as error:
            message = str(error)

            if "ambiguous" in message:
                raise HTTPException(
                    status_code=409,
                    detail=message,
                ) from error

            raise HTTPException(
                status_code=404,
                detail=message,
            ) from error

    return DisruptionResponse.model_validate(result)


# --------------------------------------------------
# 8. LLM assistant
# --------------------------------------------------

@app.post(
    "/api/assistant/ask",
    response_model=AssistantResponse,
)
def ask_assistant(request: AssistantQuestion) -> AssistantResponse:
    """Answer a natural-language question using approved graph operations."""

    try:
        with get_driver() as driver:
            result = answer_question(request.question, driver)

    except InvalidAssistantIntent as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except AuthenticationError as error:
        raise HTTPException(
            status_code=503,
            detail="The LLM service is not configured correctly.",
        ) from error

    except RateLimitError as error:
        raise HTTPException(
            status_code=503,
            detail="The LLM service is temporarily unavailable.",
        ) from error

    except APIConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the LLM service.",
        ) from error

    return AssistantResponse.model_validate(result)