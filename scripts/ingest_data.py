"""Import OpenFlights data into the FlightGraph database."""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

BATCH_SIZE = 500


# --------------------------------------------------
# 2. Define dataset columns
# --------------------------------------------------

airport_columns = [
    "airport_id",
    "name",
    "city",
    "country",
    "iata",
    "icao",
    "latitude",
    "longitude",
    "altitude",
    "timezone",
    "dst",
    "tz_database",
    "type",
    "source",
]

route_columns = [
    "airline",
    "airline_id",
    "source_airport",
    "source_airport_id",
    "destination_airport",
    "destination_airport_id",
    "codeshare",
    "stops",
    "equipment",
]


# --------------------------------------------------
# 3. Load datasets
# --------------------------------------------------

airports = pd.read_csv(
    DATA_DIR / "airports.dat",
    header=None,
    names=airport_columns,
    na_values=[r"\N"],
)

print(f"Loaded {len(airports)} airports.")

routes = pd.read_csv(
    DATA_DIR / "routes.dat",
    header=None,
    names=route_columns,
    na_values=[r"\N"],
)

print(f"Loaded {len(routes)} route records.")


# --------------------------------------------------
# 4. Clean the routes dataset
# --------------------------------------------------

# Collect all valid airport identifiers.
airport_ids = set(airports["airport_id"])

# Both airports must exist in airports.dat.
valid_sources = routes["source_airport_id"].isin(airport_ids)
valid_destinations = routes["destination_airport_id"].isin(airport_ids)

valid_routes = valid_sources & valid_destinations

# Remove routes with invalid airport references.
clean_routes = routes[valid_routes].copy()

# Remove self-loops (routes from an airport to itself).
network_routes = clean_routes[
    clean_routes["source_airport_id"]
    != clean_routes["destination_airport_id"]
].copy()

print(f"Routes after cleaning: {len(network_routes)}")


# --------------------------------------------------
# 5. Prepare airline records
# --------------------------------------------------

airline_records = (
    network_routes["airline"]
    .dropna()
    .drop_duplicates()
    .sort_values()
    .to_frame(name="code")
    .to_dict(orient="records")
)

print(f"Prepared {len(airline_records)} airline records.")


# --------------------------------------------------
# 6. Prepare airline-airport connections
# --------------------------------------------------

# An airline serves both departure and arrival airports.

source_connections = network_routes[
    ["airline", "source_airport_id"]
].rename(
    columns={"source_airport_id": "airport_id"}
)

destination_connections = network_routes[
    ["airline", "destination_airport_id"]
].rename(
    columns={"destination_airport_id": "airport_id"}
)

# Combine departure and arrival connections.
# Keep each airline-airport pair only once.
airline_airport_connections = pd.concat(
    [source_connections, destination_connections],
    ignore_index=True,
).drop_duplicates()

connection_records = airline_airport_connections.to_dict(
    orient="records"
)

print(
    f"Prepared {len(connection_records)} "
    "airline-airport connections."
)


# --------------------------------------------------
# 7. Prepare FLIES_TO airport connections (NEW)
# --------------------------------------------------

# Group routes by their source and destination airports.
# Multiple airlines can operate the same airport connection.

route_pairs = (
    network_routes.groupby(
        ["source_airport_id", "destination_airport_id"]
    )["airline"]
    .agg(
        lambda codes: sorted(
            codes.dropna().unique().tolist()
        )
    )
    .reset_index(name="airlines")
)

# Count how many distinct airlines serve each connection.
route_pairs["airline_count"] = route_pairs["airlines"].apply(len)

# Convert the resulting DataFrame into dictionaries.
route_records = route_pairs.to_dict(orient="records")

print(
    f"Prepared {len(route_records)} "
    "unique airport connections."
)


# --------------------------------------------------
# 8. Prepare airport records
# --------------------------------------------------

airport_records = airports[
    [
        "airport_id",
        "name",
        "city",
        "country",
        "iata",
        "latitude",
        "longitude",
    ]
].copy()

# Replace pandas missing values with Python None.
airport_records = airport_records.astype(object).where(
    pd.notna(airport_records),
    None,
)

# Convert the DataFrame into dictionaries.
airport_records = airport_records.to_dict(orient="records")

print(f"Prepared {len(airport_records)} airport records.")


# --------------------------------------------------
# 9. Define Cypher ingestion queries
# --------------------------------------------------

AIRPORT_QUERY = """
UNWIND $airports AS airport
MERGE (a:Airport {airport_id: airport.airport_id})
SET a.name = airport.name,
    a.city = airport.city,
    a.country = airport.country,
    a.iata = airport.iata,
    a.latitude = airport.latitude,
    a.longitude = airport.longitude
"""

COUNTRY_QUERY = """
UNWIND $airports AS airport
MATCH (a:Airport {airport_id: airport.airport_id})
MERGE (c:Country {name: airport.country})
MERGE (a)-[:LOCATED_IN]->(c)
"""

AIRLINE_QUERY = """
UNWIND $airlines AS airline
MERGE (a:Airline {code: airline.code})
"""

OPERATES_QUERY = """
UNWIND $connections AS connection
MATCH (airline:Airline {code: connection.airline})
MATCH (airport:Airport {airport_id: connection.airport_id})
MERGE (airline)-[:OPERATES]->(airport)
"""

FLIES_TO_QUERY = """
UNWIND $routes AS route
MATCH (source:Airport {airport_id: route.source_airport_id})
MATCH (destination:Airport {airport_id: route.destination_airport_id})
MERGE (source)-[r:FLIES_TO]->(destination)
SET r.airlines = route.airlines,
    r.airline_count = route.airline_count
"""


# --------------------------------------------------
# 10. Load Neo4j credentials
# --------------------------------------------------

load_dotenv()

neo4j_auth = os.getenv("NEO4J_AUTH")

if not neo4j_auth:
    raise ValueError("NEO4J_AUTH is missing.")

username, password = neo4j_auth.split("/", maxsplit=1)


# --------------------------------------------------
# 11. Connect to Neo4j and import data
# --------------------------------------------------

with GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=(username, password),
) as driver:

    driver.verify_connectivity()

    with driver.session() as session:

        # ------------------------------------------
        # 11.1 Import Airport nodes
        # ------------------------------------------

        for start in range(0, len(airport_records), BATCH_SIZE):
            batch = airport_records[start:start + BATCH_SIZE]

            session.run(
                AIRPORT_QUERY,
                airports=batch,
            ).consume()

            print(f"Imported {len(batch)} airports")

        print("Airport ingestion completed!")

        # ------------------------------------------
        # 11.2 Import Country nodes and relationships
        # ------------------------------------------

        for start in range(0, len(airport_records), BATCH_SIZE):
            batch = airport_records[start:start + BATCH_SIZE]

            session.run(
                COUNTRY_QUERY,
                airports=batch,
            ).consume()

            print(f"Imported {len(batch)} country relationships")

        print("Country ingestion completed!")

        # ------------------------------------------
        # 11.3 Import Airline nodes
        # ------------------------------------------

        for start in range(0, len(airline_records), BATCH_SIZE):
            batch = airline_records[start:start + BATCH_SIZE]

            session.run(
                AIRLINE_QUERY,
                airlines=batch,
            ).consume()

            print(f"Imported {len(batch)} airlines")

        print("Airline ingestion completed!")

        # ------------------------------------------
        # 11.4 Import OPERATES relationships
        # ------------------------------------------

        for start in range(0, len(connection_records), BATCH_SIZE):
            batch = connection_records[start:start + BATCH_SIZE]

            session.run(
                OPERATES_QUERY,
                connections=batch,
            ).consume()

            print(f"Imported {len(batch)} OPERATES relationships")

        print("OPERATES ingestion completed!")

        # ------------------------------------------
        # 11.5 Import FLIES_TO relationships
        # ------------------------------------------

        for start in range(0, len(route_records), BATCH_SIZE):
            batch = route_records[start:start + BATCH_SIZE]

            session.run(
                FLIES_TO_QUERY,
                routes=batch,
            ).consume()

            print(f"Imported {len(batch)} FLIES_TO relationships")

        print("FLIES_TO ingestion completed!")