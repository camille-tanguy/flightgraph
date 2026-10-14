"""FlightGraph REST API."""

from fastapi import FastAPI, HTTPException, Path, Query

from api.database import get_driver
from api.models import (
    AirportResponse,
    ConnectionResponse,
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

    cypher = """
    MATCH (source:Airport {iata: $iata})
    MATCH (source)-[r:FLIES_TO]->(destination:Airport)
    RETURN
        destination.iata AS iata,
        destination.name AS name,
        destination.city AS city,
        r.airline_count AS airline_count
    ORDER BY airline_count DESC, destination.airport_id
    LIMIT $limit
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

        # Retrieve direct outgoing connections.
        results = session.run(
            cypher,
            iata=iata.upper(),
            limit=limit,
        )

        connections = [
            ConnectionResponse.model_validate(dict(record))
            for record in results
        ]

    return connections


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

    cypher = """
    MATCH (source:Airport {iata: $source})
    MATCH (destination:Airport {iata: $destination})
    MATCH path = shortestPath(
        (source)-[:FLIES_TO*..10]->(destination)
    )
    RETURN
        [airport IN nodes(path) | airport.iata] AS airports,
        length(path) AS flights
    ORDER BY flights
    LIMIT 1
    """

    with get_driver() as driver, driver.session() as session:
        result = session.run(
            cypher,
            source=source.upper(),
            destination=destination.upper(),
        ).single()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No route found between these airports.",
        )

    return ShortestPathResponse.model_validate(dict(result))


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