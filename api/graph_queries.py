"""Reusable Neo4j queries for the FlightGraph application."""

from neo4j import READ_ACCESS, Driver


def find_connections(
    driver: Driver,
    iata: str,
    limit: int = 10,
) -> list[dict]:
    """Find direct outgoing flight connections from an airport."""

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

    with driver.session(default_access_mode=READ_ACCESS) as session:
        airport_exists = session.run(
            """
            MATCH (a:Airport {iata: $iata})
            RETURN count(a) > 0 AS exists
            """,
            iata=iata.upper(),
        ).single()["exists"]

        if not airport_exists:
            raise LookupError(f"Airport '{iata}' not found.")

        results = session.run(
            cypher,
            iata=iata.upper(),
            limit=limit,
        )

        return [dict(record) for record in results]


def find_shortest_route(
    driver: Driver,
    source: str,
    destination: str,
) -> dict | None:
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

    with driver.session(default_access_mode=READ_ACCESS) as session:
        result = session.run(
            cypher,
            source=source.upper(),
            destination=destination.upper(),
        ).single()

    return dict(result) if result is not None else None