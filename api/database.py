"""Neo4j database connection for FlightGraph."""

import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


def get_driver():
    """Create a Neo4j database driver."""
    neo4j_auth = os.getenv("NEO4J_AUTH")
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")

    if not neo4j_auth:
        raise ValueError("NEO4J_AUTH is missing.")

    username, password = neo4j_auth.split("/", maxsplit=1)

    return GraphDatabase.driver(
        neo4j_uri,
        auth=(username, password),
    )