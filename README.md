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
