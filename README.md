# FlightGraph — Airline Network Resilience & Disruption Simulator

FlightGraph is a graph-based application designed to analyze airline
networks, identify critical airports, and evaluate the impact of
airport closures on global connectivity.

The project combines graph database technology, network analytics,
and AI-assisted exploration to investigate how disruptions affect
airline connections and which alternative routes remain available.

## Planned Features

- **Network exploration:** Explore airport connections and reachability.
- **Shortest paths:** Find connections between airports.
- **Graph analytics:** Identify critical airports using graph algorithms.
- **Disruption simulation:** Evaluate the impact of airport closures.
- **AI assistant:** Answer natural-language questions about the network.

## Technology Stack

- Python
- Neo4j and Cypher
- Neo4j Graph Data Science
- FastAPI
- Docker and Docker Compose
- pytest
- GitHub Actions

## Project Status

🚧 In development — Milestone 0: Repository and environment setup.

## git

FlightGraph will use the historical OpenFlights dataset,
primarily `airports.dat` and `routes.dat`.

Source: <https://github.com/jpatokal/openflights>

**Note:** OpenFlights does not necessarily represent current airline connections.
Results will be interpreted accordingly.

## Database Setup

FlightGraph uses Neo4j 5.26 and the historical OpenFlights dataset.

### 1. Configure the environment

Create a `.env` file from `.env.example` and replace the placeholder
Neo4j password with your own.

### 2. Start Neo4j

```bash
docker compose up -d
```

Neo4j Browser is available at <http://localhost:7474>.

### 3. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

Use a Python virtual environment for local development.

### 4. Download the datasets

Download `airports.dat` and `routes.dat` from the
[OpenFlights GitHub repository](https://github.com/jpatokal/openflights/tree/master/data).

Place them in:

```text
data/raw/
├── airports.dat
└── routes.dat
```

### 5. Initialize the database schema

```bash
python scripts/init_db.py
```

This creates the uniqueness constraints and airport lookup index.

### 6. Import the flight network

```bash
python scripts/ingest_data.py
```

The ingestion script imports airports, countries, airlines, and their
relationships into Neo4j.

### Dataset limitations

OpenFlights contains historical route information. Connections in
FlightGraph should not be interpreted as current flight schedules.
