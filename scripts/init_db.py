"""Initialize the FlightGraph Neo4j schema."""

import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load Neo4j credentials.
load_dotenv()

neo4j_auth = os.getenv("NEO4J_AUTH")

if not neo4j_auth:
    raise ValueError("NEO4J_AUTH is missing from the environment.")

username, password = neo4j_auth.split("/", maxsplit=1)

# Read the schema file.
SCHEMA_PATH = Path(__file__).with_name("schema.cypher")
schema = SCHEMA_PATH.read_text(encoding="utf-8")

# Separate the Cypher statements.
statements = [
    statement.strip()
    for statement in schema.split(";")
    if statement.strip()
]

# Connect to Neo4j.
with GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=(username, password),
) as driver:

    driver.verify_connectivity()

    # Execute each Cypher statement.
    with driver.session() as session:
        for statement in statements:
            session.run(statement).consume()
            print("Schema statement executed successfully.")

print("FlightGraph database schema initialized!")