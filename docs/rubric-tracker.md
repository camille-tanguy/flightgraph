# FlightGraph — Evaluation Tracker

## Project Information

- **Project:** FlightGraph — Airline Network Resilience & Disruption Simulator
- **Developer:** Camille Tanguy
- **Repository:** <https://github.com/camille-tanguy/flightgraph>
- **Target:** Level 2 engineering depth
- **Time budget:** 40–50 hours
- **Current milestone:** 4 — Graph Analytics & Disruption Simulation
- **Current branch:** `feat/graph-analytics-disruption`
- **Development approach:** Solo project with feature branches and pull requests

---

## 1. Progress Summary

| Metric | Value |
| --- | --- |
| Total available points | 100 |
| Verified rubric points | Reassessment in progress |
| Current milestone | 4 |
| Overall status | IN PROGRESS |
| Completed development milestones | 0, 1, 2, 3 |
| Milestone 4 status | IMPLEMENTED — final delivery pending |
| Automated tests | 10 passing |
| Git workflow | Feature branches + merged pull requests |
| Database | Neo4j 5.26 |
| Graph analytics | Neo4j Graph Data Science |
| Backend | FastAPI + Pydantic |
| Infrastructure | Docker Compose |

### Current Technology Stack

- Python 3.13.3
- Neo4j 5.26
- Cypher
- Neo4j Graph Data Science
- FastAPI
- Pydantic
- Docker
- Docker Compose
- Git and GitHub
- pytest
- pandas
- python-dotenv

### Planned Technologies

- GitHub Actions
- pytest-cov
- Pylint
- Makefile
- Nginx
- LLM integration
- Validated NL-to-Cypher

---

## 2. Status Definitions

| Status | Meaning |
| --- | --- |
| NOT STARTED | The requirement has not been implemented |
| IMPLEMENTED | The requirement exists but has not been fully verified |
| VALIDATED | The requirement has been tested against available evidence |

**Important:** A validated requirement is supported by project evidence, but
the professor determines the official grade.

The internal score must only include sufficiently verified criteria.

---

## 3. Professor's Evaluation Checklist

## 3.1 Docker Infrastructure & Services — 9 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Docker Compose with at least 3 services | 2 | NOT STARTED | Currently using Neo4j service |
| Proper Dockerfile or official image | 2 | VALIDATED | Official Neo4j Docker image |
| `.env.example`, no committed secrets | 2 | IMPLEMENTED | `.env.example` and `.gitignore` |
| At least one image on a public registry | 2 | NOT STARTED | Planned for Milestone 7 |
| Docker Compose starts cleanly | 1 | VALIDATED | Neo4j container successfully started |

### Remaining Work

- Add FastAPI container.
- Add Nginx reverse proxy.
- Configure at least three Docker Compose services.
- Publish an application image to a public container registry.
- Verify that no credentials are committed.
- Test clean installation from scratch.

---

## 3.2 Neo4j Database — 10 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| At least 3 node labels and 3 relationship types | 3 | VALIDATED | Airport, Airline, Country; FLIES_TO, OPERATES, LOCATED_IN |
| At least 2 relevant constraints | 2 | VALIDATED | 3 uniqueness constraints |
| Appropriate database indexes | 2 | VALIDATED | Airport IATA index |
| Dataset ingestion script | 2 | VALIDATED | `scripts/ingest_data.py` |
| Dataset source documented and justified | 1 | IMPLEMENTED | OpenFlights exploration and README |

### Validated Database Structure

**Node labels:**

- `Airport`
- `Airline`
- `Country`

**Relationship types:**

- `FLIES_TO`
- `OPERATES`
- `LOCATED_IN`

### Database Measurements

| Element | Count |
| --- | ---: |
| Airport nodes | 7,698 |
| Airline nodes | 566 |
| Country nodes | 237 |
| Total nodes | 8,501 |
| FLIES_TO relationships | 36,906 |
| OPERATES relationships | 19,146 |
| LOCATED_IN relationships | 7,698 |
| Total relationships | 63,750 |

### Database Design Decisions

- Airports are uniquely identified by OpenFlights airport IDs.
- IATA codes are not assumed to be globally unique.
- Flight connections are directed.
- Multiple airlines operating the same connection are aggregated.
- Historical OpenFlights data is not treated as live flight information.

Remaining Work

- Complete the graph modeling rationale.
- Add the final graph schema diagram.
- Demonstrate index usage through `EXPLAIN` and `PROFILE`.

---

## 3.3 FastAPI — 6 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| At least 4 endpoints, including advanced graph queries | 2 | VALIDATED | Airport, connections, pathfinding, reachability, disruption |
| Pydantic input/output validation | 2 | VALIDATED | Request parameters and response models |
| Functional Swagger documentation | 1 | VALIDATED | `/docs` tested |
| Proper HTTP error handling | 1 | IMPLEMENTED | HTTP 404, 409, 422 tested in relevant endpoints |

### Implemented API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Check API status |
| GET | `/api/airports/{iata}` | Retrieve airport information |
| GET | `/api/airports/{iata}/connections` | Retrieve direct outgoing connections |
| GET | `/api/routes/shortest` | Find shortest flight path |
| GET | `/api/airports/{iata}/reachable` | Find reachable airports |
| GET | `/api/disruptions/airports/{iata}` | Simulate airport closure |

 Remaining Work

- Improve consistency of error handling.
- Handle ambiguous IATA codes across all endpoints.
- Add additional database failure tests.
- Document response examples.

---

## 3.4 Advanced Cypher — 9 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Pathfinding or GDS algorithms in at least 2 endpoints | 4 | VALIDATED | Shortest-path and disruption endpoints |
| Complex graph-pattern matching | 3 | IMPLEMENTED | Directed routes and multi-hop reachability |
| `WITH`, `UNWIND`, subqueries, aggregations | 2 | IMPLEMENTED | Graph analytics queries; complete requirement needs verification |

### Implemented Graph Queries

- Direct airport connections.
- Shortest-path search.
- Multi-hop reachability.
- PageRank ranking.
- Weakly Connected Components.
- Airport closure analysis.

 Remaining Work

- Verify all required Cypher constructs are demonstrated.
- Add representative advanced queries to `demo.ipynb`.
- Explain query complexity.
- Include performance evidence.

---

## 3.5 Optimization & Performance — 5 Points

| Requirement | Points | Status | Evidence |
| --- | ---: ---|---|
| Optimized queries, parameterization, indexes, and benchmarks | 5 | IMPLEMENTED | Parameterized queries and indexes; benchmarks pending |

### Current Improvements

- Parameterized Cypher queries.
- Uniqueness constraints and relevant indexes.
- Bounded graph traversals.
- GDS graph projections for analytics.
- Temporary projection cleanup.

 Remaining Work

- Measure query execution times.
- Compare indexed and non-indexed queries.
- Demonstrate `EXPLAIN` and `PROFILE`.
- Benchmark disruption simulations.
- Document performance limitations.

---

## 3.6 Graph Data Science & Agentic — 13 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| GDS graph projection and at least 2 algorithms | 2 | VALIDATED | PageRank and WCC |
| Genuine ML prediction/classification workflow | 3 | NOT STARTED | Milestone 5 |
| LangGraph, GraphRAG, or NL-to-Cypher | 4 | NOT STARTED | Milestone 6 |
| LLM reliability, validation, and guardrails | 4 | NOT STARTED | Milestone 6 |

### Validated GDS Projection

**Graph name:** `flightgraph`

| Metric | Value |
| --- | ---: |
| Airport nodes | 7,698 |
| Directed relationships | 36,906 |

### Algorithm 1 — PageRank

**Status:** VALIDATED

Purpose:

Identify structurally influential airports in the historical airline network.

Observed examples:

| Airport | IATA | Approximate PageRank |
| --- | --- | ---: |
| Atlanta | ATL | 14.997 |
| Chicago O'Hare | ORD | 13.742 |
| Atatürk International | ISL | 13.654 |
| Denver | DEN | 13.572 |

These values were observed during the Neo4j Browser analysis.

**Limitation:** PageRank measures structural influence, not necessarily
the impact of an airport closure.

### Algorithm 2 — Weakly Connected Components

**Status:** VALIDATED

Purpose:

Identify connected groups of airports when flight direction is ignored.

### Validated Baseline

| Metric | Value |
| --- | ---: |
| Total airports | 7,698 |
| Connected components | 4,491 |
| Largest component | 3,188 |
| Isolated airports | 4,484 |

### Interpretation

Most airports with recorded connections belong to one large connected
component.

Many other airports are isolated because the historical dataset contains
airport records without corresponding routes.

WCC does not establish directed passenger reachability.

---

## 3.7 Schemas & Modeling — 7 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Neo4j graph-schema diagram | 2 | NOT STARTED | Planned |
| System architecture diagram | 2 | NOT STARTED | Planned |
| Modeling rationale and anti-genericity appendix | 3 | IMPLEMENTED | Modeling decisions explored; appendix pending |

 Remaining Work

- Create Neo4j graph schema diagram.
- Create system architecture diagram.
- Compare our schema with a generic AI-generated schema.
- Explain modeling trade-offs.
- Document the decision to aggregate direct airport relationships.

---

## 3.8 Documentation — 5 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Comprehensive README with screenshots | 3 | IMPLEMENTED | README exists; final documentation pending |
| Demonstration notebook (`demo.ipynb`) | 2 | NOT STARTED | Planned for Milestone 8 |

 Remaining Work

- Complete installation instructions.
- Add screenshots.
- Document all API endpoints.
- Document GDS installation.
- Include actual simulation results.
- Create demonstration notebook.

---

## 3.9 Clean Code — 4 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| `.pylintrc`, pylint >= 9.5, `make lint` | 2 | NOT STARTED | Planned |
| PEP 8 and clean architecture | 1 | IMPLEMENTED | Separate API, database, and disruption modules |
| Appropriate docstrings | 1 | IMPLEMENTED | Functions and modules documented |

 Remaining Work

- Install and configure Pylint.
- Create `.pylintrc`.
- Achieve a measured score >= 9.5/10.
- Implement `make lint`.
- Resolve code-quality warnings.

**Important:** The professor specifies a potentially significant penalty
for failing the Pylint requirement.

---

## 3.10 Makefile & Automation — 3 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Makefile containing required commands | 1 | NOT STARTED | Planned |
| Functional commands and `make help` | 1 | NOT STARTED | Planned |
| Makefile usage documented | 1 | NOT STARTED | Planned |

### Required Commands

- `make help`
- `make install`
- `make run`
- `make docker-run`
- `make test`
- `make lint`
- `make clean`

 Remaining Work

Implement and verify every command.

---

## 3.11 Tests & Quality — 10 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Unit, API, and Neo4j connectivity tests | 3 | IMPLEMENTED | API tests and database connectivity verification |
| Neo4j and FastAPI container health checks | 2 | NOT STARTED | Milestone 7 |
| Cypher query tests runnable through `make test` | 2 | NOT STARTED | Milestone 7 |
| Test coverage >= 60% | 2 | NOT STARTED | Coverage not measured |
| All tests pass with a coverage report | 1 | IMPLEMENTED | 10 tests passing; coverage report pending |

### Validated Automated Tests

*Current result: 10 passing tests**

Tests cover:

- API health check.
- Invalid airport codes.
- Invalid connection limits.
- Successful airport lookup.
- Airport-not-found responses.
- Disruption request validation.
- Unknown airport handling.
- Ambiguous IATA codes.
- Successful disruption responses.
- Cleanup attempt after simulated WCC failure.

 Remaining Work

- Measure coverage with pytest-cov.
- Reach >= 60% coverage.
- Add Neo4j integration tests.
- Add Cypher query tests.
- Verify container health checks.
- Integrate tests into GitHub Actions.

---

## 3.12 Software Engineering Best Practices — 9 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| GitHub Actions lint workflow | 1 | NOT STARTED | Planned |
| GitHub Actions test workflow with coverage | 1 | NOT STARTED | Planned |
| README badges | 1 | NOT STARTED | Planned |
| Documented code reviews | 1 | IMPLEMENTED | Solo PR review process; professor clarification pending |
| Reverse proxy or authentication | 3 | NOT STARTED | Nginx planned |
| `EXPLAIN` / `PROFILE` optimization | 2 | NOT STARTED | Milestone 8 |

Remaining Work

- Configure GitHub Actions.
- Add test and lint workflows.
- Add status badges.
- Implement Nginx reverse proxy.
- Document query optimization.
- Clarify solo code-review expectations.

---

## 3.13 Collaboration & Git Management — 10 Points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Feature branches and branch workflow | 2 | VALIDATED | Multiple development branches and PRs |
| Proper `.gitignore` | 1 | VALIDATED | `.gitignore` committed |
| Balanced contribution distribution | 3 | NOT STARTED | Solo-project clarification required |
| At least one substantial merged PR per member | 3 | VALIDATED | Multiple merged feature PRs |
| Clear commit messages | 1 | IMPLEMENTED | Meaningful commit history |

### Verified Workflow

- `main` is the stable branch.
- Development occurs on feature branches.
- Pull requests are used to merge completed milestones.
- Commits describe meaningful changes.

### Relevant Pull Requests

- PR #1: Initial repository setup.
- PR #4: Neo4j schema and ingestion.
- Milestone 3: FastAPI backend PR merged.
- Milestone 4: Graph analytics PR pending.

Repository:

<https://github.com/camille-tanguy/flightgraph>

### Outstanding Question

The professor's collaboration requirements were written for teams.

The project is being developed independently.

Clarification is required regarding:

- Balanced contributions.
- Self-reviews.
- Required number of PRs.
- Solo grading rules.

No additional contributors or reviews should be fabricated.

---

## 4. Scoring Summary

The maximum score is 100 points.

The status assessment has been updated, but the complete internal
point-by-point score has not yet been independently recalculated.

| Category | Maximum Points | Score Status |
| --- | ---: | --- |
| Docker Infrastructure | 9 | Partially validated |
| Neo4j Database | 10 | Mostly validated |
| FastAPI | 6 | Mostly validated |
| Advanced Cypher | 9 | Partially validated |
| Optimization & Performance | 5 | Pending benchmarks |
| GDS & Agentic | 13 | 2-point GDS criterion validated |
| Schemas & Modeling | 7 | In progress |
| Documentation | 5 | In progress |
| Clean Code | 4 | In progress |
| Makefile & Automation | 3 | Not started |
| Tests & Quality | 10 | Partially validated |
| Software Engineering Best Practices | 9 | In progress |
| Collaboration & Git Management | 10 | Mostly validated; solo clarification |
| **TOTAL** | **100** | **Reassessment pending** |

**This table is a progress assessment, not an official grade.**

Before final submission, recalculate the verified score using the exact
rubric criteria and supporting evidence.

---

## 5. Milestone Progress

| Milestone | Status |
| --- | --- |
| 0. GitHub Repository & Environment Setup | VALIDATED |
| 1. Dataset Feasibility & Graph Modeling | VALIDATED |
| 2. Neo4j Setup & Data Ingestion | VALIDATED |
| 3. FastAPI & Advanced Cypher | VALIDATED for tested functionality |
| 4. Graph Analytics & Disruption Simulation | IMPLEMENTED |
| 5. Machine Learning Workflow | NOT STARTED |
| 6. AI Assistant & Guardrails | NOT STARTED |
| 7. Docker Integration, Testing & CI/CD | NOT STARTED |
| 8. Optimization, Documentation & Demo | NOT STARTED |

---

## 6. Milestone 4 — Graph Analytics & Disruption Simulation

## Objective

Develop a graph-based simulator capable of evaluating the structural
impact of closing an airport.

The simulator addresses the research question:

> How can graph analytics identify critical airports, evaluate network
> disruptions, and recommend alternative connections?

## Implemented Features

- Neo4j GDS integration.
- Airport graph projection.
- PageRank analysis.
- Weakly Connected Components analysis.
- Temporary disruption graph creation.
- Single-airport closure simulation.
- Comparison of connectivity metrics.
- Temporary graph cleanup.
- FastAPI disruption endpoint.
- Pydantic response validation.
- Automated API and failure-path tests.

## Architecture

The implementation separates responsibilities across modules.

| File | Responsibility |
| --- | --- |
| `api/main.py` | FastAPI endpoints |
| `api/database.py` | Neo4j connection |
| `api/models.py` | Pydantic response models |
| `api/disruption.py` | Disruption simulation logic |
| `tests/test_disruption.py` | Disruption-related tests |
| `compose.yaml` | Neo4j and GDS configuration |

## Validated CDG Closure Simulation

**Closed airport:** Paris Charles de Gaulle International Airport

**IATA:** CDG

**OpenFlights airport ID:** 1382

### Network Comparison

| Metric | Before | After | Change |
| --- | ---: | ---: | ---: |
| Airports | 7,698 | 7,697 | -1 |
| Directed flight connections | 36,906 | 36,436 | -470 |
| Connected components | 4,491 | 4,492 | +1 |
| Largest connected component | 3,188 | 3,186 | -2 |
| Isolated airports | 4,484 | 4,485 | +1 |

 Interpretation

Closing CDG removes 470 directed airport-to-airport connections
from the historical OpenFlights network.

The number of weakly connected components increases by one.

The largest connected component decreases by two airports.

One airport is removed by the closure itself, while another airport
loses membership in the largest component.

An exploratory component-membership comparison identified
Ovda International Airport (VDA) as the additional affected airport.

This finding has not yet been automated in the API response

### Important Limitations

- The dataset represents historical routes.
- Simulations do not model actual flight cancellations.
- WCC ignores relationship direction.
- Connectivity does not guarantee realistic passenger itineraries.
- PageRank does not directly measure closure impact.
- The API currently returns aggregate disruption metrics.
- Alternative route recommendations are not yet implemented.
- GDS projections require available memory.
- Simultaneous simulation performance has not been benchmarked.

## Verified Tests

- 10 automated tests passed.
- CDG simulation successfully executed from Python.
- CDG disruption endpoint returned HTTP 200.
- Temporary graph cleanup was verified after successful execution.
- Failure-path cleanup attempt was tested using mocks.

Remaining Work

- Complete README documentation.
- Review code quality and error handling.
- Commit and push the feature branch.
- Create the Milestone 4 pull request.
- Merge into `main`.
- Synchronize the local repository.

## Completion Criteria

Milestone 4 can be marked VALIDATED for its agreed scope when:

- [x] GDS projection works.
- [x] PageRank works.
- [x] WCC works.
- [x] CDG closure simulation works.
- [x] FastAPI integration works.
- [x] Automated tests pass.
- [x] Successful simulation cleanup is verified.
- [x] Failure-path cleanup attempt is tested.
- [ ] Documentation is complete.
- [ ] GitHub pull request is merged.

---

## 7. Remaining Development Milestones

## Milestone 5 — Machine Learning

**Status:** NOT STARTED

Objective

Implement a genuine, defensible classification or prediction workflow.

### Initial Candidate

Airport-route link prediction.

### Required Feasibility Analysis

- Dataset suitability.
- Feature engineering.
- Negative sampling.
- Train/test splitting.
- Data leakage prevention.
- Model selection.
- Evaluation metrics.
- Interpretation of results.

### Decision Requirement

Do not implement link prediction without first evaluating
whether the available data supports a meaningful experiment.

If unsuitable, select and justify an alternative ML task.

---

## Milestone 6 — AI Assistant & Guardrails

**Status:** NOT STARTED

Objective

Enable users to ask natural-language questions about the flight network.

### Planned Approach

Validated NL-to-Cypher.

### Requirements

- Natural-language question interpretation.
- Approved Cypher query generation or selection.
- Read-only database permissions.
- Query validation.
- Rejection of unsafe operations.
- Evidence-grounded responses.
- Structured outputs.
- Successful-query tests.
- Guardrail rejection tests.

### Design Principle

Prefer a constrained, reliable assistant over a complex autonomous agent.

---

## Milestone 7 — Infrastructure, Testing & CI/CD

**Status:** NOT STARTED

### Planned Work

- Three-service Docker Compose setup.
- FastAPI container.
- Neo4j container.
- Nginx reverse proxy.
- Container health checks.
- Public container image.
- GitHub Actions.
- Pylint.
- pytest coverage.
- Makefile commands.
- Reproducible installation.

### Quality Targets

- Pylint >= 9.5/10.
- Test coverage >= 60%.
- All tests passing.
- Clean Docker Compose startup.
- No exposed credentials.

---

## Milestone 8 — Optimization & Final Delivery

**Status:** NOT STARTED

Planned Work

- Query optimization.
- `EXPLAIN` and `PROFILE`.
- Graph schema diagram.
- Architecture diagram.
- Modeling rationale.
- Anti-genericity appendix.
- Complete README.
- Screenshots.
- `demo.ipynb`.
- Final rubric audit.
- Live demonstration preparation.

---

## 8. Important Grading Risks

| Risk | Potential Penalty | Priority |
| --- | --- | --- |
| Non-functional Makefile commands | -3 points | HIGH |
| Missing `.pylintrc` or pylint below 9.5 | -8 points | CRITICAL |
| Non-functional application | Up to -25 points | CRITICAL |
| Missing functional agentic component | -15 points | CRITICAL |
| Generic or unjustified graph schema | Up to -5 points | HIGH |
| Exposed credentials | -5 points per secret/file | CRITICAL |
| Missing substantial merged PR | -3 points per member | HIGH |
| Contribution below 10% | -5 points | SOLO CLARIFICATION |
| Plagiarism | 0/100 and administrative report | CRITICAL |

## Risk Mitigation

- Keep the application functional throughout development.
- Test after each major change.
- Verify every Makefile command.
- Prioritize reliable AI guardrails.
- Implement genuine ML.
- Never commit secrets.
- Document modeling decisions.
- Use feature branches and pull requests.
- Record measured results rather than invented metrics.
- Clarify solo grading requirements with the professor.

---

## 9. Outstanding Questions

## Solo Project Grading

The professor's rubric contains team collaboration requirements.

Clarification is still needed regarding:

1. Balanced commit contributions.
2. Code reviews for solo projects.
3. Substantial merged PR requirements.
4. Acceptance of self-reviews.

## Machine Learning

Questions to resolve before implementing link prediction:

1. Does the historical dataset support a meaningful prediction task?
2. Which graph-derived features are appropriate?
3. How can negative samples be constructed defensibly?
4. How can data leakage be prevented?
5. Which evaluation metrics are appropriate?
6. What limitations must be disclosed?

## Graph Analytics

Future improvements to consider:

1. Performance benchmarking.
2. Directed reachability impact.
3. Additional affected-airport reporting.
4. Alternative connections after airport closures.

These improvements should only be implemented when justified by
grading value, engineering value, and available time.

---

## 10. Project Management Principles

1. Prioritize the professor's official grading rubric.
2. Keep the project achievable within 40–50 hours.
3. Favor readable and maintainable code.
4. Implement and validate features incrementally.
5. Maintain a stable `main` branch.
6. Use meaningful feature branches and commits.
7. Explain technical decisions and trade-offs.
8. Never invent benchmark or ML results.
9. Never expose credentials.
10. Track implementation separately from validation.
11. Keep documentation synchronized with the application.
12. Build a professional GitHub portfolio project.

---

## 11. Next Action

**Current task:** Complete Milestone 4 delivery.

1. Finalize README documentation.
2. Run automated tests.
3. Review Git changes.
4. Commit the graph analytics and disruption simulator.
5. Push `feat/graph-analytics-disruption`.
6. Create and merge the pull request.
7. Synchronize `main`.
8. Start Milestone 5 — Machine Learning Feasibility.

**Next milestone:** 5 — Machine Learning Workflow.
