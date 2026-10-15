"""Service orchestration for the FlightGraph LLM assistant."""

from neo4j import Driver

from api.assistant_llm import interpret_question
from api.assistant_validation import validate_intent
from api.disruption import simulate_airport_closure
from api.graph_queries import find_connections, find_shortest_route


def answer_question(question: str, driver: Driver) -> dict:
    """Interpret a question and execute an approved graph operation."""

    intent = interpret_question(question)
    validated_intent = validate_intent(intent)

    operation = validated_intent.operation
    source = validated_intent.source_iata

    if operation == "SIMULATE_CLOSURE":
        result = simulate_airport_closure(driver, source)

        return {
            "operation": operation,
            "parameters": {"iata": source},
            "data": result,
        }

    if operation == "GET_CONNECTIONS":
        connections = find_connections(
            driver,
            source,
            limit=10,
        )

        return {
            "operation": operation,
            "parameters": {"iata": source},
            "data": {"connections": connections},
        }

    if operation == "FIND_SHORTEST_ROUTE":
        destination = validated_intent.destination_iata

        route = find_shortest_route(
            driver,
            source,
            destination,
        )

        if route is None:
            raise LookupError(
                f"No route found between {source} and {destination}."
            )

        return {
            "operation": operation,
            "parameters": {
                "source": source,
                "destination": destination,
            },
            "data": route,
        }

    raise ValueError(f"Unsupported operation: {operation}")
