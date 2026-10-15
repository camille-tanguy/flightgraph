# FlightGraph — Airline Network Resilience & Disruption Simulator

FlightGraph is a graph-based application designed to analyze airline
networks, identify critical airports, and evaluate the impact of airport
closures on global connectivity.

The project combines graph database technology, network analytics,
machine learning, and AI-assisted exploration to investigate how
disruptions affect airline connections.

**Research question:**

> How can graph analytics and AI identify critical airports, evaluate
> network disruptions, and recommend alternative connections?

FlightGraph uses historical OpenFlights data and is intended for
network analysis and educational experimentation, not real-time
flight planning.

---

## Features

FlightGraph implements five main functionalities:

- **Network exploration:** Explore airport connections and multi-hop reachability.
- **Shortest paths:** Find connections between airports using graph traversal.
- **Graph analytics:** Identify structurally influential airports using PageRank and Weakly Connected Components.
- **Disruption simulation:** Evaluate how closing an airport affects network connectivity.
- **AI assistant:** Answer natural-language questions through validated, predefined graph operations.

The project also includes a supervised machine learning experiment
for airport-route link prediction.

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

**Milestone 8 — Final Testing, Documentation, and Submission Preparation*

The core application has been implemented and tested locally.

Implemented components include:

- Historical OpenFlights data ingestion into Neo4j.
- Graph schema, constraints, and indexes.
- FastAPI endpoints for airport exploration and shortest routes.
- PageRank and Weakly Connected Components analytics.
- Single-airport closure simulation.
- Automatic recovery of missing GDS graph projections.
- Supervised route link-prediction experiment.
- AI assistant with validated, predefined graph operations.
- Three-service Docker Compose architecture.
- Nginx reverse proxy and container health checks.
- Automated testing and code-quality checks.
- Multi-platform Docker image publishing through GitHub Actions.
- Architecture and graph schema documentation.
- Interactive demonstration notebook.

Remaining work focuses on final documentation, screenshots,
rubric verification, and live demonstration preparation.

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

**FastAPI** validates requests, executes application logic, and
communicates with Neo4j.

**Neo4j** stores the airline network and provides graph querying
and analytics capabilities.

Neo4j Graph Data Science runs as a plugin inside the Neo4j service.

Docker Compose manages service networking, startup dependencies,
and health checks.

For further details, see the
[System Architecture documentation](docs/architecture.md).

---

## Quick Start — Docker Compose

### Prerequisites

To run FlightGraph locally, install:

- Git
- Docker Desktop with Docker Compose

Python 3.13 is also needed for local development, database ingestion,
and testing.

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

The OpenAI API key is optional for the core graph functionality
but required for AI assistant requests.

**Security:** Never commit `.env` or API credentials to GitHub.

### 3. Start the application

Build and start the three Docker services:

```bash
make docker-run
```

Alternatively:

```bash
docker compose up -d --build --wait
```

The first startup may take longer because Docker needs to
download images and install dependencies.

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

Swagger provides an interactive interface for exploring and
testing the API endpoints.

**Important:** Starting Docker Compose does not automatically
download or import the OpenFlights dataset.

Follow the database setup instructions below to populate
a new Neo4j database.

### 6. Stop the application

```bash
make down
```

Alternatively:

```bash
docker compose down
```

Neo4j data is stored in a persistent Docker volume.

Do not use `docker compose down -v` unless you explicitly intend
to remove the database volume and its stored data.

---

## Public Docker Image

FlightGraph publishes a public, multi-platform Docker image
for its FastAPI backend.

**Image:**

```text
ghcr.io/camille-tanguy/flightgraph-api:latest
```

Download the image using:

```bash
docker pull ghcr.io/camille-tanguy/flightgraph-api:latest
```

Supported architectures:

- `linux/amd64` — Intel/AMD systems.
- `linux/arm64` — ARM-based systems, including Apple Silicon.

The image is automatically built and published through GitHub Actions
when relevant changes are merged into `main`.

**Important:** The published image contains the FastAPI application,
not the complete three-service environment.

The full application also requires Neo4j and Nginx, which are
configured through Docker Compose.

[View the public FlightGraph Docker image](https://github.com/camille-tanguy/flightgraph/pkgs/container/flightgraph-api)

---

## Dataset

FlightGraph uses the historical OpenFlights dataset.

Primary files:

- `airports.dat`
- `routes.dat`

Additional airline information may be derived from OpenFlights data.

**Source:** [OpenFlights GitHub Repository](https://github.com/jpatokal/openflights)

OpenFlights contains historical airline route information and does
not necessarily represent currently operated routes.

FlightGraph results should therefore be interpreted as structural
analyses of the recorded network rather than real-time aviation information.

---

## Database Setup

FlightGraph uses Neo4j 5.26 and the OpenFlights dataset.

The following instructions initialize a new database.

### 1. Start Neo4j

If the complete Docker application is not already running,
start the database:

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

Install project dependencies:

```bash
make install
```

Equivalent command:

```bash
python -m pip install -r requirements.txt
```

The ingestion scripts run on your local machine and connect
to Neo4j through `localhost:7687`, as configured in `.env`.

### 3. Download the datasets

Download `airports.dat` and `routes.dat` from the
[OpenFlights data directory](https://github.com/jpatokal/openflights/tree/master/data).

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

This script creates the database constraints and indexes
used by FlightGraph.

### 5. Import the flight network

```bash
python scripts/ingest_data.py
```

The ingestion process imports airports, countries, airlines,
and the relevant graph relationships.

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

These figures correspond to the project's validated dataset
and ingestion configuration.

Results may differ if the source data or ingestion rules change.

---

## Graph Database Model

FlightGraph uses three node labels:

- `Airport`
- `Airline`
- `Country`

And three relationship types:

- `FLIES_TO`
- `OPERATES`
- `LOCATED_IN`

The main analytical relationship is:

```text
(Airport)-[:FLIES_TO]->(Airport)
```

Connections are directed because a recorded connection from
airport A to airport B does not necessarily imply the reverse.

Multiple airlines operating the same airport pair are
aggregated into relationship properties.

This modeling approach prioritizes network analysis rather
than individual flight operations.

Database constraints include unique airport identifiers,
airline codes, and country names.

An additional index supports airport searches by IATA code.

For details, see:

- [Graph Database Schema](docs/graph-schema.md)
- [Modeling Rationale and Anti-Genericity Analysis](docs/modeling-rationale.md)

---

## REST API

FlightGraph provides a REST API built with FastAPI
and connected to Neo4j.

Pydantic is used to validate requests and structure API responses.

### Running the API

**Recommended: Docker Compose*

```bash
make docker-run
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
make run
```

Access Swagger at:

<http://127.0.0.1:8000/docs>

If port 8000 is unavailable, use:

```bash
make run PORT=8001
```

Access the local API at:

<http://127.0.0.1:8001/docs>

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

The interactive Swagger interface provides request schemas
and response documentation for all endpoints.

### API Limitations

- FlightGraph uses historical OpenFlights data, not live flight schedules.
- Shortest routes minimize the number of flight connections, not travel time or ticket price.
- IATA codes are not guaranteed to uniquely identify airports in the underlying dataset.
- The reachability endpoint returns a maximum of 20 destinations.
- Route availability does not imply that a route is currently operated.

---

## Graph Analytics & Disruption Simulation

FlightGraph uses Neo4j Graph Data Science (GDS) to analyze
airline network connectivity and evaluate the structural impact
of airport closures.

### Graph Algorithms

Two GDS algorithms are implemented.

**PageRank*

Identifies structurally influential airports based on their
position in the directed flight network.

PageRank measures network importance but does not directly
quantify the consequences of closing an airport.

**Weakly Connected Components (WCC)*

Identifies connected groups of airports while ignoring
relationship direction.

WCC helps measure structural fragmentation but does not
establish whether passengers can travel between two airports
following the direction of available flights.

### Graph Projection

The validated GDS projection contains:

- **7,698 airports**
- **36,906 directed airport-to-airport connections**

The projection includes Airport nodes and FLIES_TO relationships.

It excludes Airline and Country nodes because the main
analytical task concerns airport network connectivity.

### Airport Closure Simulation

FlightGraph supports single-airport closure simulations.

Example:

```http
GET /api/disruptions/airports/CDG
```

The simulator:

1. Identifies the airport using its unique OpenFlights ID.
2. Ensures that the baseline GDS projection exists.
3. Creates a temporary GDS graph excluding the selected airport.
4. Calculates connectivity metrics using WCC.
5. Compares baseline and disrupted networks.
6. Deletes the temporary graph after the simulation.

The simulation does not permanently delete airports or
relationships from Neo4j.

**Reliability improvement:**

GDS projections exist in memory and may disappear after
Neo4j restarts.

FlightGraph checks whether the baseline projection exists
and recreates it automatically when necessary.

This behavior was verified by removing the baseline projection,
calling the disruption API, and confirming successful recovery.

### Validated Example: CDG Closure

| Metric | Before | After | Change |
| --- | ---: | ---: | ---: |
| Airports | 7,698 | 7,697 | -1 |
| Directed connections | 36,906 | 36,436 | -470 |
| Connected components | 4,491 | 4,492 | +1 |
| Largest component | 3,188 | 3,186 | -2 |
| Isolated airports | 4,484 | 4,485 | +1 |

Removing CDG eliminates 470 directed connections but causes
limited additional fragmentation in the historical network
under the WCC metric.

### Limitations

- OpenFlights contains historical routes, not live flight schedules.
- WCC ignores flight direction and therefore cannot establish actual passenger reachability.
- PageRank measures structural influence, not necessarily disruption impact.
- Simulations model network structure, not operational flight cancellations.
- Temporary GDS projections consume memory during execution.

---

## Machine Learning — Airport Route Link Prediction

FlightGraph includes a supervised machine learning experiment
investigating whether graph-structural features improve the
identification of historical airline connections compared
with geographic distance alone.

### Methodology

- **Dataset:** Historical OpenFlights network containing 3,214 active airports and 36,906 directed connections.
- **Task:** Binary classification of recorded and unrecorded directed routes.
- **Split:** Approximately 80/20, grouping reciprocal routes together.
- **Negative sampling:** Balanced positive and negative examples.
- **Model:** Logistic Regression with standardized features.
- **Baseline:** Geographic distance.
- **Graph-enhanced model:** Geographic distance, source out-degree, destination in-degree, and common neighbors.

Graph features are calculated from the training network
to reduce data leakage.

Positive training examples are evaluated with their candidate
edges excluded from feature calculations.

### Results

| Metric | Baseline | Graph-enhanced |
| --- | ---: | ---: |
| Initial ROC-AUC | 0.9357 | **0.9922** |
| Initial F1-score | 0.8748 | **0.9685** |
| Distance-restricted ROC-AUC | 0.7801 | **0.9531** |
| Distance-restricted F1-score | 0.6667 | **0.8696** |

Graph-derived features improved route identification
under both negative-sampling strategies.

Limitations

The dataset is historical, and unrecorded connections are
treated as negative examples.

The class distribution is artificially balanced, and results
depend on the negative-sampling strategy.

The distance-restricted experiment is exploratory rather
than an independent validation.

Training-positive feature construction also differs from
held-out test feature construction.

These models do not forecast future flight routes or
estimate real-world route probabilities.

### Notebook

See
[`notebooks/02_route_link_prediction.ipynb`](notebooks/02_route_link_prediction.ipynb)
for the experimental methodology, feature engineering,
model training, evaluation, and robustness analysis.

---

## AI Assistant

FlightGraph includes an AI-assisted interface for exploring
the airline network through natural-language questions.

The assistant uses an LLM to interpret requests and map them
to approved graph operations.

Rather than executing arbitrary LLM-generated Cypher queries,
FlightGraph validates the requested operation before interacting
with Neo4j.

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

Its responses are limited by the supported operations and
the historical nature of the underlying dataset.

---

## Testing and Code Quality

FlightGraph uses automated tests and static code analysis
to maintain software quality.

### Run Tests

```bash
make test
```

### Run Linters

```bash
make lint
```

### Verified Quality Metrics

The following results were verified locally on October 15, 2026:

| Metric | Result |
| --- | ---: |
| Automated tests | **26 passing** |
| Test coverage | **64.74%** |
| Pylint score | **10.00/10** |
| Ruff | **Passing** |

These measurements describe the verified local project state
and may change as development continues.

### Continuous Integration

FlightGraph uses GitHub Actions to automatically verify
pull requests.

The CI workflow:

1. Installs Python and project dependencies.
2. Executes Ruff.
3. Executes Pylint with a minimum score of 9.5/10.
4. Runs pytest with a minimum coverage threshold of 60%.

The publishing workflow builds and uploads the FastAPI
Docker image to GitHub Container Registry.

Images are published for AMD64 and ARM64 architectures.

---

## Development Commands

The project includes a Makefile for frequently used
development tasks.

| Command | Description |
| --- | --- |
| `make help` | Display available commands |
| `make install` | Install Python dependencies |
| `make run` | Start FastAPI locally |
| `make docker-run` | Build and start Docker services |
| `make test` | Run tests and coverage |
| `make lint` | Run Ruff and Pylint |
| `make up` | Start Docker services |
| `make down` | Stop Docker services |
| `make logs` | Follow Docker container logs |
| `make clean` | Remove temporary files and caches |

Example development workflow:

```bash
make install
make test
make lint
```

To launch the Docker application:

```bash
make docker-run
```

To remove generated Python caches and test artifacts:

```bash
make clean
```

---

## Technical Documentation

FlightGraph includes technical documentation covering its
architecture, database model, engineering decisions, and
query performance.

| Document | Description |
| --- | --- |
| [System Architecture](docs/architecture.md) | Docker services, FastAPI, Neo4j, and application components |
| [Graph Database Schema](docs/graph-schema.md) | Node labels, relationships, constraints, and indexes |
| [Modeling Rationale](docs/modeling-rationale.md) | Schema alternatives, design trade-offs, and anti-genericity analysis |
| [Query Optimization](docs/query-optimization.md) | Cypher execution plans and performance analysis |
| [Demonstration Notebook](demo.ipynb) | Interactive walkthrough of FlightGraph's main features |
| [Machine Learning Notebook](notebooks/02_route_link_prediction.ipynb) | Route link-prediction experiment and evaluation |

These documents provide additional evidence of the project's
technical implementation and engineering decisions.

---

## Demonstration

FlightGraph includes an interactive Jupyter notebook:

[`demo.ipynb`](demo.ipynb)

The notebook demonstrates:

1. API health verification.
2. Airport exploration.
3. Direct connections.
4. Shortest-path queries.
5. Multi-hop reachability.
6. Airport closure simulation.
7. Graph analytics.
8. Machine learning results.
9. Optional AI assistant interaction.

### Running the demonstration

Start the Docker services:

```bash
make docker-run
```

Ensure the OpenFlights dataset has been imported into Neo4j.

Open `demo.ipynb` in VS Code or Jupyter.

Select the Python environment containing the project's
dependencies.

Run the notebook cells in order.

The AI assistant demonstration is optional and requires
a configured OpenAI API key.

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

The repository's software licensing and the licensing terms
applicable to the underlying dataset should be considered separately.
