"""Verify that FlightGraph can connect to Neo4j."""

import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

neo4j_auth = os.getenv("NEO4J_AUTH")

if not neo4j_auth:
    raise ValueError("NEO4J_AUTH is missing from the environment.")

username, password = neo4j_auth.split("/", maxsplit=1)

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=(username, password),
)

driver.verify_connectivity()

print("Successfully connected to Neo4j!")

with driver.session() as session:
    result = session.run("RETURN 'Hello from Python!' AS message")
    record = result.single()
    print(record["message"])

driver.close()