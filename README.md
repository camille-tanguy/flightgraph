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

## REST API

FlightGraph provides a REST API built with FastAPI and connected to Neo4j.

### Run the API

Start the Neo4j database:

```bash
docker compose up -d
```

Activate the Python virtual environment and start FastAPI:

```bash
python -m uvicorn api.main:app --reload
```

Interactive API documentation is available at:

<http://127.0.0.1:8000/docs>

### Available endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Check API status |
| GET | `/api/airports/{iata}` | Retrieve airport information |
| GET | `/api/airports/{iata}/connections` | Find direct flight connections |
| GET | `/api/routes/shortest` | Find a shortest route between airports |
| GET | `/api/airports/{iata}/reachable` | Find airports reachable within a maximum number of flights |

### Example requests

Retrieve Paris Charles de Gaulle Airport:

```http
GET /api/airports/CDG
```

Find a shortest route from Paris to New York:

```http
GET /api/routes/shortest?source=CDG&destination=JFK
```

Find airports reachable from Paris within one flight:

```http
GET /api/airports/CDG/reachable?max_hops=1
```

### Run automated tests

```bash
python -m pytest tests/ -v
```

The API uses Pydantic for input and response validation.

### Data limitations

FlightGraph uses historical OpenFlights route data, not live flight schedules.

Shortest routes minimize the number of flight connections, not travel time or ticket price.

IATA codes are not guaranteed to uniquely identify airports in the underlying dataset.

The reachability endpoint currently returns a maximum of 20 destinations.

## Graph Analytics & Disruption Simulation

FlightGraph uses Neo4j Graph Data Science (GDS) to analyze airline
network connectivity and evaluate the structural impact of airport closures.

### Graph Algorithms

Two GDS algorithms are implemented:

- **PageRank:** Identifies structurally influential airports based on
  their position in the directed flight network.
- **Weakly Connected Components (WCC):** Identifies connected groups
  of airports while ignoring flight direction.

The GDS projection contains:

- 7,698 airports
- 36,906 directed airport-to-airport connections

### Airport Closure Simulation

FlightGraph supports read-only simulations of single-airport closures.

Example:

```http
GET /api/disruptions/airports/CDG
```

The simulator:

1. Identifies the airport using its unique OpenFlights ID.
2. Creates a temporary GDS graph excluding that airport.
3. Calculates connectivity metrics using WCC.
4. Compares baseline and disrupted networks.
5. Deletes the temporary graph after the simulation.

### Validated Example: CDG Closure

| Metric | Before | After | Change |
| --- | ---: | ---: | ---: |
| Airports | 7,698 | 7,697 | -1 |
| Directed connections | 36,906 | 36,436 | -470 |
| Connected components | 4,491 | 4,492 | +1 |
| Largest component | 3,188 | 3,186 | -2 |
| Isolated airports | 4,484 | 4,485 | +1 |

The simulation indicates that removing CDG causes limited fragmentation
of the historical flight network despite eliminating 470 directed connections.

### Limitations

- OpenFlights contains historical routes, not live flight schedules.
- WCC ignores flight direction and therefore cannot establish actual
  passenger reachability.
- PageRank measures structural influence, not necessarily disruption impact.
- Simulations model network structure, not operational flight cancellations.
- Temporary GDS projections consume memory during execution.

## Machine Learning — Airport Route Link Prediction

FlightGraph includes a supervised machine learning experiment investigating
whether graph-structural features improve the identification of historical
airline connections compared with geographic distance alone.

### Methodology

- **Dataset:** Historical OpenFlights network (3,214 active airports;
  36,906 directed connections).
- **Task:** Binary classification of recorded and unrecorded directed routes.
- **Split:** Approximately 80/20, grouping reciprocal routes together.
- **Negative sampling:** Balanced positive and negative examples.
- **Models:** Logistic Regression with standardized features.
- **Baseline:** Geographic distance.
- **Graph-enhanced:** Geographic distance, source out-degree,
  destination in-degree, and common neighbors.

Graph features are calculated from the training network to reduce
data leakage. Positive training examples are evaluated with their
candidate edges excluded from feature calculations.

### Results

| Metric | Baseline | Graph-enhanced |
| --- | ---: | ---: |
| Initial ROC-AUC | 0.9357 | **0.9922** |
| Initial F1-score | 0.8748 | **0.9685** |
| Distance-restricted ROC-AUC | 0.7801 | **0.9531** |
| Distance-restricted F1-score | 0.6667 | **0.8696** |

Graph-derived features improved route identification under both
negative-sampling strategies.

Limitations

The dataset is historical, and unrecorded connections are treated
as negative examples. The class distribution is artificially balanced,
and results depend on the negative-sampling strategy.

The distance-restricted experiment is exploratory rather than an
independent validation. Training-positive feature construction also
differs from held-out test feature construction.

These models do not forecast future flight routes or estimate
real-world route probabilities.

### Notebook

See [`notebooks/02_route_link_prediction.ipynb`](notebooks/02_route_link_prediction.ipynb)
for the experimental methodology, feature engineering, model training,
evaluation, and robustness analysis.
