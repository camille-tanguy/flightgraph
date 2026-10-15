# FlightGraph — Airline Network Resilience & Disruption Simulator

FlightGraph is a graph-based application designed to analyze airline networks, identify critical airports, and evaluate the impact of airport closures on global connectivity.

The project combines graph database technology, network analytics, machine learning, and AI-assisted exploration to investigate how disruptions affect airline connections and which alternative routes remain available.

**Research question:**

> How can graph analytics and AI identify critical airports, evaluate network disruptions, and recommend alternative connections?

FlightGraph uses historical OpenFlights data and is intended for network analysis and educational experimentation, not real-time flight planning.

---

## Features

FlightGraph implements five main functionalities:

- **Network exploration:** Explore airport connections and multi-hop reachability.
- **Shortest paths:** Find connections between airports using graph traversal.
- **Graph analytics:** Identify structurally influential airports using PageRank and Weakly Connected Components.
- **Disruption simulation:** Evaluate how closing an airport affects network connectivity.
- **AI assistant:** Answer natural-language questions through validated, predefined graph operations.

The project also includes a supervised machine learning experiment for airport-route link prediction.

## Technology Stack

| Component | Technology |
| --- | --- |
| Programming language | Python 3.13 |
| Graph database | Neo4j 5.26 |
| Graph queries | Cypher |
| Graph analytics | Neo4j Graph Data Science |
| REST API | FastAPI and Pydantic |
| Machine learning | scikit-learn |
| Containerization | Docker and Docker Compose |
| Reverse proxy | Nginx |
| Testing | pytest and pytest-cov |
| Code quality | Ruff and Pylint |
| Continuous Integration | GitHub Actions |
| Container registry | GitHub Container Registry |
| AI integration | OpenAI API |

## Project Status

**In development — Milestone 7: Infrastructure, Testing & CI/CD*

Implemented components include:

- Historical OpenFlights data ingestion into Neo4j.
- Graph schema, constraints, and indexes.
- FastAPI endpoints for airport exploration and shortest routes.
- PageRank and Weakly Connected Components analytics.
- Single-airport closure simulation.
- Supervised route link-prediction experiment.
- AI assistant with validated, predefined graph operations.
- Three-service Docker Compose architecture.
- Nginx reverse proxy and container health checks.
- Automated testing and code-quality checks.
- Multi-platform Docker image publishing through GitHub Actions.

Milestone 8 will focus on optimization, documentation, architecture diagrams, and the final demonstration.

---

## Architecture

FlightGraph uses a three-service architecture managed by Docker Compose.

```text
                    Client / Browser
                           |
                           | HTTP
                           v
                 +-------------------+
                 |       Nginx       |
                 |   Reverse Proxy   |
                 |  localhost:8080   |
                 +---------+---------+
                           |
                           | HTTP
                           v
                 +-------------------+
                 |      FastAPI      |
                 |  Application API  |
                 |   Internal :8000  |
                 +---------+---------+
                           |
                           | Bolt
                           v
                 +-------------------+
                 |       Neo4j       |
                 |   Graph Database  |
                 |   Internal :7687  |
                 +---------+---------+
                           |
                           v
                    Persistent Volume
                       neo4j_data
```

**Nginx** receives incoming HTTP requests and forwards them to FastAPI.

**FastAPI** validates requests, executes application logic, and communicates with Neo4j.

**Neo4j** stores the airline network and provides graph querying and analytics capabilities.

Docker Compose manages service networking, startup dependencies, and health checks.

---

## Quick Start — Docker Compose

### Prerequisites

To run FlightGraph locally, install:

- Git
- Docker Desktop with Docker Compose

Python 3.13 is also needed for local development, database ingestion, and testing.

### 1. Clone the repository

```bash
git clone https://github.com/camille-tanguy/flightgraph.git
cd flightgraph
```

### 2. Configure environment variables

Create a local environment file:

```bash
cp .env.example .env
```

Open `.env` and configure your Neo4j credentials.

For example:

```dotenv
NEO4J_AUTH=neo4j/replace_with_your_password
NEO4J_URI=bolt://localhost:7687

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

Replace the example password with your own.

The OpenAI API key is optional for the core graph functionality but required for AI assistant requests.

**Security:** Never commit `.env` or API credentials to GitHub.

### 3. Start the application

Build and start the three Docker services:

```bash
docker compose up -d --build --wait
```

Alternatively:

```bash
make up
```

Note that `make up` starts the containers without waiting for all health checks to finish.

The first startup may take longer because Docker needs to download images and install dependencies.

### 4. Verify the services

Check container status:

```bash
docker compose ps
```

All three services should eventually report `healthy`:

- `flightgraph-neo4j`
- `flightgraph-api`
- `flightgraph-nginx`

Test the API health endpoint:

```bash
curl http://localhost:8080/health
```

Expected response:

```json
{
  "status": "ok"
}
```

### 5. Access FlightGraph

| Service | Address |
| --- | --- |
| FastAPI Swagger documentation | <http://localhost:8080/docs> |
| API health endpoint | <http://localhost:8080/health> |
| Neo4j Browser | <http://localhost:7474> |

Swagger provides an interactive interface for exploring and testing the API endpoints.

**Important:** Starting Docker Compose does not automatically download or import the OpenFlights dataset.

Follow the database setup instructions below to populate a new Neo4j database.

### 6. Stop the application

```bash
make down
```

Alternatively:

```bash
docker compose down
```

Neo4j data is stored in a persistent Docker volume.

Do not use `docker compose down -v` unless you explicitly intend to remove the database volume and its stored data.

---

## Public Docker Image

FlightGraph publishes a public, multi-platform Docker image for its FastAPI backend.

**Image:**

`ghcr.io/camille-tanguy/flightgraph-api:latest`

Download the image using:

```bash
docker pull ghcr.io/camille-tanguy/flightgraph-api:latest
```

Supported architectures:

- `linux/amd64` — Intel/AMD systems
- `linux/arm64` — ARM-based systems, including Apple Silicon

The image is automatically built and published through GitHub Actions when relevant changes are merged into `main`.

**Important:** The published image contains the FastAPI application, not the complete three-service environment.

The full application also requires Neo4j and Nginx, which are configured through Docker Compose.

[View the public FlightGraph Docker image](https://github.com/camille-tanguy/flightgraph/pkgs/container/flightgraph-api)

---

## Dataset

FlightGraph uses the historical OpenFlights dataset.

Primary files:

- `airports.dat`
- `routes.dat`

Additional airline information may be derived from OpenFlights data.

**Source:** [OpenFlights GitHub Repository](https://github.com/jpatokal/openflights)

OpenFlights contains historical airline route information and does not necessarily represent currently operated routes.

FlightGraph results should therefore be interpreted as structural analyses of the recorded network rather than real-time aviation information.

---

## Database Setup

FlightGraph uses Neo4j 5.26 and the OpenFlights dataset.

The following instructions initialize a new database.

### 1. Start Neo4j

If the complete Docker application is not already running, start the database:

```bash
docker compose up -d neo4j
```

Neo4j Browser is available at:

<http://localhost:7474>

### 2. Install Python dependencies

Create and activate a Python virtual environment.

On macOS or Linux:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

The ingestion scripts run on your local machine and connect to Neo4j through `localhost:7687`, as configured in `.env`.

### 3. Download the datasets

Download `airports.dat` and `routes.dat` from the [OpenFlights data directory](https://github.com/jpatokal/openflights/tree/master/data).

Place the files in:

```text
data/raw/
├── airports.dat
└── routes.dat
```

### 4. Initialize the database schema

```bash
python scripts/init_db.py
```

This script creates the database constraints and indexes used by FlightGraph.

### 5. Import the flight network

```bash
python scripts/ingest_data.py
```

The ingestion process imports airports, countries, airlines, and the relevant graph relationships.

### 6. Verify the database

Open Neo4j Browser and execute:

```cypher
MATCH (a:Airport)
RETURN count(a) AS airport_count;
```

To count direct airport-to-airport relationships:

```cypher
MATCH ()-[r:FLIES_TO]->()
RETURN count(r) AS connection_count;
```

The validated project dataset contained:

| Metric | Value |
| --- | ---: |
| Airports | 7,698 |
| Directed airport connections | 36,906 |

These figures correspond to the project's validated dataset and ingestion configuration.

Results may differ if the source data or ingestion rules change.

---

## REST API

FlightGraph provides a REST API built with FastAPI and connected to Neo4j.

Pydantic is used to validate requests and structure API responses.

### Running the API

**Recommended: Docker Compose*

```bash
docker compose up -d --build --wait
```

Access Swagger at:

<http://localhost:8080/docs>

**Alternative: Local FastAPI development*

Start Neo4j:

```bash
docker compose up -d neo4j
```

Then run FastAPI locally:

```bash
python -m uvicorn api.main:app --reload
```

Access Swagger at:

<http://127.0.0.1:8000/docs>

### Available Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Check API status |
| GET | `/api/airports/{iata}` | Retrieve airport information |
| GET | `/api/airports/{iata}/connections` | Find direct flight connections |
| GET | `/api/routes/shortest` | Find a shortest route |
| GET | `/api/airports/{iata}/reachable` | Find reachable airports |
| GET | `/api/disruptions/airports/{iata}` | Simulate an airport closure |
| POST | `/api/assistant/ask` | Ask a natural-language question |

### Example Requests

Retrieve information about Paris Charles de Gaulle Airport:

```http
GET /api/airports/CDG
```

Find a shortest route between Paris and New York:

```http
GET /api/routes/shortest?source=CDG&destination=JFK
```

Find airports reachable from CDG within one flight:

```http
GET /api/airports/CDG/reachable?max_hops=1
```

Simulate the closure of CDG:

```http
GET /api/disruptions/airports/CDG
```

The interactive Swagger interface provides request schemas and response documentation for all endpoints.

### API Limitations

- FlightGraph uses historical OpenFlights data, not live flight schedules.
- Shortest routes minimize the number of flight connections, not travel time or ticket price.
- IATA codes are not guaranteed to uniquely identify airports in the underlying dataset.
- The reachability endpoint returns a maximum of 20 destinations.
- Route availability does not imply that a route is currently operated.

---

## Graph Analytics & Disruption Simulation

FlightGraph uses Neo4j Graph Data Science (GDS) to analyze airline network connectivity and evaluate the structural impact of airport closures.

### Graph Algorithms

Two GDS algorithms are implemented.

**PageRank*

Identifies structurally influential airports based on their position in the directed flight network.

PageRank measures network importance but does not directly quantify the consequences of closing an airport.

**Weakly Connected Components (WCC)*

Identifies connected groups of airports while ignoring relationship direction.

WCC helps measure structural fragmentation but does not establish whether passengers can travel between two airports following the direction of available flights.

### Graph Projection

The validated GDS projection contains:

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

The simulation does not permanently delete airports or relationships from Neo4j.

### Validated Example: CDG Closure

| Metric | Before | After | Change |
| --- | ---: | ---: | ---: |
| Airports | 7,698 | 7,697 | -1 |
| Directed connections | 36,906 | 36,436 | -470 |
| Connected components | 4,491 | 4,492 | +1 |
| Largest component | 3,188 | 3,186 | -2 |
| Isolated airports | 4,484 | 4,485 | +1 |

Removing CDG eliminates 470 directed connections but causes limited additional fragmentation in the historical network under the WCC metric.

### Limitations

- OpenFlights contains historical routes, not live flight schedules.
- WCC ignores flight direction and therefore cannot establish actual passenger reachability.
- PageRank measures structural influence, not necessarily disruption impact.
- Simulations model network structure, not operational flight cancellations.
- Temporary GDS projections consume memory during execution.

---

## Machine Learning — Airport Route Link Prediction

FlightGraph includes a supervised machine learning experiment investigating whether graph-structural features improve the identification of historical airline connections compared with geographic distance alone.

### Methodology

- **Dataset:** Historical OpenFlights network containing 3,214 active airports and 36,906 directed connections.
- **Task:** Binary classification of recorded and unrecorded directed routes.
- **Split:** Approximately 80/20, grouping reciprocal routes together.
- **Negative sampling:** Balanced positive and negative examples.
- **Model:** Logistic Regression with standardized features.
- **Baseline:** Geographic distance.
- **Graph-enhanced model:** Geographic distance, source out-degree, destination in-degree, and common neighbors.

Graph features are calculated from the training network to reduce data leakage.

Positive training examples are evaluated with their candidate edges excluded from feature calculations.

### Results

| Metric | Baseline | Graph-enhanced |
| --- | ---: | ---: |
| Initial ROC-AUC | 0.9357 | **0.9922** |
| Initial F1-score | 0.8748 | **0.9685** |
| Distance-restricted ROC-AUC | 0.7801 | **0.9531** |
| Distance-restricted F1-score | 0.6667 | **0.8696** |

Graph-derived features improved route identification under both negative-sampling strategies.

 Limitations

The dataset is historical, and unrecorded connections are treated as negative examples.

The class distribution is artificially balanced, and results depend on the negative-sampling strategy.

The distance-restricted experiment is exploratory rather than an independent validation.

Training-positive feature construction also differs from held-out test feature construction.

These models do not forecast future flight routes or estimate real-world route probabilities.

### Notebook

See [`notebooks/02_route_link_prediction.ipynb`](notebooks/02_route_link_prediction.ipynb) for the experimental methodology, feature engineering, model training, evaluation, and robustness analysis.

---

## AI Assistant

FlightGraph includes an AI-assisted interface for exploring the airline network through natural-language questions.

The assistant uses an LLM to interpret requests and map them to approved graph operations.

Rather than executing arbitrary LLM-generated Cypher queries, FlightGraph validates the requested operation before interacting with Neo4j.

### Design Principles

- **Restricted operations:** Only supported graph operations can be executed.
- **Input validation:** Requests are checked before database access.
- **Read-only behavior:** The assistant does not provide unrestricted database modification capabilities.
- **Evidence-grounded responses:** Answers are based on retrieved graph data.
- **Error handling:** Unsupported requests and provider failures produce structured API errors.

### Endpoint

```http
POST /api/assistant/ask
```

The request body contains a natural-language question.

For example:

```json
{
  "question": "What are the direct connections from CDG?"
}
```

The assistant requires a configured OpenAI API key.

Its responses are limited by the supported operations and the historical nature of the underlying dataset.

---

## Testing and Code Quality

FlightGraph uses automated tests and static code analysis to maintain software quality.

### Run Tests

```bash
make test
```

### Run Linters

```bash
make lint
```

### Verified Quality Metrics

The following results were obtained during Milestone 7:

| Metric | Result |
| --- | ---: |
| Automated tests | 24 passing |
| Test coverage | 63.58% |
| Pylint score | 9.64/10 |
| Ruff | Passing |

These measurements describe the validated project state at the time of testing and may change as development continues.

### Continuous Integration

FlightGraph uses GitHub Actions to automatically verify Pull Requests.

The CI workflow:

1. Installs Python and project dependencies.
2. Executes Ruff.
3. Executes Pylint with a minimum score of 9.5/10.
4. Runs pytest with a minimum coverage threshold of 60%.

The publishing workflow builds and uploads the FastAPI Docker image to GitHub Container Registry.

Images are published for AMD64 and ARM64 architectures.

---

## Development Commands

The project includes a Makefile for frequently used development tasks.

| Command | Description |
| --- | --- |
| `make help` | Display available commands |
| `make test` | Run tests and coverage |
| `make lint` | Run Ruff and Pylint |
| `make up` | Start Docker services |
| `make down` | Stop Docker services |
| `make logs` | Follow Docker container logs |

---

## Project Limitations

FlightGraph is an educational graph analytics application.

Its main limitations include:

- Historical rather than real-time aviation data.
- Route existence does not imply current operational availability.
- No flight schedules, pricing, or passenger demand data.
- Connectivity metrics do not fully represent airline operational resilience.
- Single-airport closure simulations do not model cascading operational effects.
- Machine learning results depend on negative sampling and evaluation assumptions.
- The AI assistant supports a restricted set of graph operations.
- The local Docker setup uses HTTP and is not intended as a production-secured public deployment.

These limitations should be considered when interpreting results.

---

## License and Data Attribution

FlightGraph uses the historical OpenFlights dataset.

Original dataset:

<https://github.com/jpatokal/openflights>

The dataset is attributed to its original maintainers.

The repository's software licensing and the licensing terms applicable to the underlying dataset should be considered separately.
