"""Airport disruption analysis using Neo4j Graph Data Science."""

## Perform the disruption analysis

from uuid import uuid4

from neo4j import Driver


def find_airport(driver: Driver, iata: str) -> dict:
    """Retrieve an airport using its IATA code."""

    query = """
    MATCH (airport:Airport {iata: $iata})
    RETURN
        airport.airport_id AS airport_id,
        airport.name AS name,
        airport.iata AS iata
    ORDER BY airport.airport_id
    LIMIT 2
    """

    with driver.session() as session:
        records = list(
            session.run(query, iata=iata.upper())
        )

    if not records:
        raise ValueError(f"Airport '{iata}' not found.")

    if len(records) > 1:
        raise ValueError(
            f"Airport code '{iata}' is ambiguous."
        )

    return dict(records[0])


def create_disruption_graph(
    driver: Driver,
    airport_id: int,
    graph_name: str,
) -> dict:
    """Create a temporary GDS graph excluding one airport."""

    query = """
    MATCH (source:Airport)
    WHERE source.airport_id <> $airport_id

    OPTIONAL MATCH (source)-[:FLIES_TO]->(destination:Airport)
    WHERE destination.airport_id <> $airport_id

    WITH gds.graph.project(
        $graph_name,
        source,
        destination
    ) AS projection

    RETURN
        projection.graphName AS graph_name,
        projection.nodeCount AS airport_count,
        projection.relationshipCount AS route_count
    """

    with driver.session() as session:
        result = session.run(
            query,
            airport_id=airport_id,
            graph_name=graph_name,
        ).single()

    if result is None:
        raise RuntimeError("Failed to create disruption graph.")

    return dict(result)

def get_connectivity_metrics(
    driver: Driver,
    graph_name: str,
) -> dict:
    """Calculate connectivity metrics for a projected GDS graph."""

    query = """
    CALL gds.wcc.stream($graph_name)
    YIELD nodeId, componentId

    WITH componentId, count(nodeId) AS component_size

    RETURN
        count(*) AS total_components,
        max(component_size) AS largest_component,
        sum(component_size) AS total_airports,
        count(
            CASE WHEN component_size = 1 THEN 1 END
        ) AS isolated_airports
    """

    with driver.session() as session:
        result = session.run(
            query,
            graph_name=graph_name,
        ).single()

    if result is None:
        raise RuntimeError(
            f"Failed to calculate connectivity for '{graph_name}'."
        )

    return dict(result)



def get_graph_relationship_count(
    driver: Driver,
    graph_name: str,
) -> int:
    """Return the relationship count of an existing GDS graph."""

    query = """
    CALL gds.graph.list($graph_name)
    YIELD relationshipCount
    RETURN relationshipCount
    """

    with driver.session() as session:
        result = session.run(
            query,
            graph_name=graph_name,
        ).single()

    if result is None:
        raise RuntimeError(f"GDS graph '{graph_name}' not found.")

    return result["relationshipCount"]

def ensure_baseline_graph(driver: Driver) -> None:
    """Create the baseline GDS projection if it does not exist."""

    query = """
    CALL gds.graph.exists('flightgraph')
    YIELD exists
    RETURN exists
    """

    with driver.session() as session:
        exists = session.run(query).single()["exists"]

        if exists:
            return

        session.run(
            """
            CALL gds.graph.project(
                'flightgraph',
                'Airport',
                {
                    FLIES_TO: {
                        orientation: 'NATURAL'
                    }
                }
            )
            """
        ).consume()


def simulate_airport_closure(driver: Driver, iata: str) -> dict:
    """Simulate an airport closure without modifying stored graph data."""

    # 1. Identify the airport.
    airport = find_airport(driver, iata)
    airport_id = airport["airport_id"]

    # 2. Generate a unique temporary graph name.
    graph_name = f"disruption_{uuid4().hex}"

    try:
        # 3. Ensure the baseline GDS projection is available.
        ensure_baseline_graph(driver)

        # 4. Calculate the original network's connectivity.
        baseline = get_connectivity_metrics(driver, "flightgraph")
        baseline_route_count = get_graph_relationship_count(
            driver,
            "flightgraph",
        )

        # 4. Create the network without the selected airport.
        disrupted_graph = create_disruption_graph(
            driver,
            airport_id,
            graph_name,
        )

        # 5. Calculate connectivity after the closure.
        disrupted = get_connectivity_metrics(driver, graph_name)

        # 6. Compare the two networks.
        return {
            "closed_airport": airport,
            "lost_routes": (
                baseline_route_count - disrupted_graph["route_count"]
                ),
            "baseline": baseline,
            "disrupted": disrupted,
            "changes": {
                "components": (
                    disrupted["total_components"]
                    - baseline["total_components"]
                ),
                "largest_component": (
                    disrupted["largest_component"]
                    - baseline["largest_component"]
                ),
                "isolated_airports": (
                    disrupted["isolated_airports"]
                    - baseline["isolated_airports"]
                ),
            },
        }

    finally:
    # Delete the temporary graph only if it exists.
        with driver.session() as session:
            session.run(
                """
                CALL gds.graph.exists($graph_name)
                YIELD exists
                WITH exists
                WHERE exists
                CALL gds.graph.drop($graph_name, false)
                YIELD graphName
                RETURN graphName
                """,
                graph_name=graph_name,
            ).consume()
