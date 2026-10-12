# FlightGraph — Evaluation Tracker

## Project Information

- **Project:** FlightGraph — Airline Network Resilience & Disruption Simulator
- **Developer:** Camille Tanguy
- **Target:** Level 2 engineering depth
- **Time budget:** 40–50 hours
- **Current milestone:** 0 — Repository & Environment Setup
- **Repository:** <https://github.com/camille-tanguy/flightgraph>

## Progress Summary

| Metric | Value |
| --- | --- |
| Total available points | 100 |
| Verified rubric points | 1/100 (conservative internal assessment) |
| Current milestone | 0 |
| Overall status | IN PROGRESS |
| Development workflow | Git feature branches + Pull Requests |
| Current technologies | Python, Git, GitHub |
| Planned technologies | Neo4j, Cypher, FastAPI, Docker, GDS, LLM |

## Status Definitions

- **NOT STARTED:** The requirement has not been implemented.
- **IMPLEMENTED:** The requirement exists but has not been fully verified.
- **VALIDATED:** The requirement has been checked against the professor's criteria.

A requirement should only be marked VALIDATED when sufficient evidence
demonstrates that it satisfies the evaluation criteria.

The verified score is an internal progress indicator, not an official grade.

---

## Evidence

### GitHub Repository

- Repository: <https://github.com/camille-tanguy/flightgraph>
- Initial setup PR: <https://github.com/camille-tanguy/flightgraph/pull/1>

### Environment

- Python 3.13.3
- Git 2.39.5
- Python virtual environment: `.venv`
- Initial dependencies: FastAPI, Uvicorn, pytest

### Git Workflow

- Stable branch: `main`
- First development branch: `chore/project-setup`
- Current documentation branch: `docs/rubric-tracking`
- First Pull Request: merged

---

# Evaluation Checklist

## 1. Docker Infrastructure & Services — 9 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| `docker-compose.yml` with at least 3 services | 2 | NOT STARTED | — |
| Proper `Dockerfile` or official image | 2 | NOT STARTED | — |
| `.env.example`, no secrets committed | 2 | IMPLEMENTED | `.env.example` |
| At least one image on a public registry | 2 | NOT STARTED | — |
| Docker Compose starts cleanly | 1 | NOT STARTED | — |

**Validated points: 0/9**

## 2. Neo4j Database — 10 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| At least 3 node labels and 3 relationship types | 3 | NOT STARTED | — |
| At least 2 relevant database constraints | 2 | NOT STARTED | — |
| Appropriate indexes for frequent queries | 2 | NOT STARTED | — |
| Dataset ingestion script | 2 | NOT STARTED | — |
| Dataset source documented and justified | 1 | NOT STARTED | — |

**Validated points: 0/10**

## 3. FastAPI — 6 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| At least 4 endpoints, including 3 advanced graph queries | 2 | NOT STARTED | — |
| Pydantic input/output validation | 2 | NOT STARTED | — |
| Functional Swagger documentation at `/docs` | 1 | NOT STARTED | — |
| Proper HTTP error handling | 1 | NOT STARTED | — |

**Validated points: 0/6**

## 4. Advanced Cypher — 9 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Pathfinding or GDS algorithms in at least 2 endpoints | 4 | NOT STARTED | — |
| Complex graph-pattern matching | 3 | NOT STARTED | — |
| `WITH`, `UNWIND`, subqueries, and aggregations | 2 | NOT STARTED | — |

**Validated points: 0/9**

## 5. Optimization & Performance — 5 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Optimized queries, parameterization, indexes, and benchmarks | 5 | NOT STARTED | — |

**Validated points: 0/5**

## 6. Graph Data Science & Agentic — 13 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| GDS graph projection and at least 2 algorithms | 2 | NOT STARTED | — |
| Genuine ML link-prediction or classification workflow | 3 | NOT STARTED | — |
| LangGraph, GraphRAG, or NL-to-Cypher component | 4 | NOT STARTED | — |
| LLM reliability, validation, and guardrails | 4 | NOT STARTED | — |

**Validated points: 0/13**

## 7. Schemas & Modeling — 7 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Neo4j graph-schema diagram | 2 | NOT STARTED | — |
| System architecture diagram | 2 | NOT STARTED | — |
| Modeling rationale and anti-genericity appendix | 3 | NOT STARTED | — |

**Validated points: 0/7**

## 8. Documentation — 5 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Comprehensive README with screenshots | 3 | IMPLEMENTED | `README.md` — initial version only |
| Demonstration notebook (`demo.ipynb`) | 2 | NOT STARTED | — |

**Validated points: 0/5**

## 9. Clean Code — 4 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| `.pylintrc`, pylint ≥ 9.5/10, functional `make lint` | 2 | NOT STARTED | — |
| PEP 8 and clean architecture | 1 | NOT STARTED | — |
| Appropriate docstrings | 1 | NOT STARTED | — |

**Validated points: 0/4**

## 10. Makefile & Automation — 3 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Makefile containing required commands | 1 | NOT STARTED | — |
| Functional commands and clear `make help` | 1 | NOT STARTED | — |
| Makefile usage documented in README | 1 | NOT STARTED | — |

**Validated points: 0/3**

### Required Makefile Commands

The final Makefile should provide:

- `make help`
- `make install`
- `make run`
- `make docker-run`
- `make test`
- `make lint`
- `make clean`

Additional commands may be implemented when justified.

## 11. Tests & Quality — 10 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| Unit, API, and Neo4j connectivity tests | 3 | NOT STARTED | — |
| Neo4j and FastAPI container health checks | 2 | NOT STARTED | — |
| Cypher query tests runnable through `make test` | 2 | NOT STARTED | — |
| Test coverage ≥ 60% | 2 | NOT STARTED | — |
| All tests pass with a coverage report | 1 | NOT STARTED | — |

**Validated points: 0/10**

## 12. Software Engineering Best Practices — 9 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| GitHub Actions lint workflow | 1 | NOT STARTED | — |
| GitHub Actions test workflow with coverage | 1 | NOT STARTED | — |
| README build, test, and coverage badges | 1 | NOT STARTED | — |
| Documented code reviews | 1 | IMPLEMENTED | Initial PR self-review |
| Reverse proxy or authentication | 3 | NOT STARTED | — |
| Index optimization demonstrated with `EXPLAIN` / `PROFILE` | 2 | NOT STARTED | — |

**Validated points: 0/9**

## 13. Collaboration & Git Management — 10 points

| Requirement | Points | Status | Evidence |
| --- | ---: | --- | --- |
| At least 2 active branches and feature-branch workflow | 2 | IMPLEMENTED | PR #1 |
| Proper `.gitignore` | 1 | VALIDATED | `.gitignore`, PR #1 |
| Balanced contribution distribution | 3 | NOT STARTED | Solo-project clarification required |
| At least 1 substantial merged PR per member | 3 | IMPLEMENTED | PR #1 — scope to be assessed |
| Clear commit messages | 1 | IMPLEMENTED | Git commit history |

**Validated points: 1/10**

---

# Scoring Summary

| Category | Maximum Points | Validated Points |
| --- | ---: | ---: |
| Docker Infrastructure | 9 | 0 |
| Neo4j Database | 10 | 0 |
| FastAPI | 6 | 0 |
| Advanced Cypher | 9 | 0 |
| Optimization & Performance | 5 | 0 |
| GDS & Agentic | 13 | 0 |
| Schemas & Modeling | 7 | 0 |
| Documentation | 5 | 0 |
| Clean Code | 4 | 0 |
| Makefile & Automation | 3 | 0 |
| Tests & Quality | 10 | 0 |
| Software Engineering Best Practices | 9 | 0 |
| Collaboration & Git Management | 10 | 1 |
| **TOTAL** | **100** | **1** |

## Current Verified Score

**1/100 points independently validated against the checklist.**

This is a conservative internal progress measurement.

It is not an official grade or a prediction of the final result.

---

# Important Grading Risks

The professor's specification identifies several possible penalties.

| Risk | Potential Penalty | Priority |
| --- | --- | --- |
| Non-functional required Makefile commands | -3 points | HIGH |
| Missing `.pylintrc` or pylint score below 9.5 | -8 points | CRITICAL |
| Non-functional application | Up to -25 points | CRITICAL |
| Missing functional agentic component | -15 points | CRITICAL |
| Generic, unjustified graph schema | Up to -5 points | HIGH |
| Exposed credentials | -5 points per secret/file | CRITICAL |
| Missing substantial merged PR | -3 points per member | HIGH |
| Contribution below 10% | -5 points | SOLO CLARIFICATION |
| Plagiarism | 0/100 and administrative report | CRITICAL |

## Risk Mitigation Strategy

- Keep the application functional throughout development.
- Introduce automated testing progressively.
- Verify the Makefile commands before submission.
- Maintain pylint compliance throughout implementation.
- Implement and test the NL-to-Cypher component.
- Document modeling decisions and rejected alternatives.
- Never commit secrets or credentials.
- Use feature branches and meaningful Pull Requests.
- Record actual measurements rather than inventing results.

---

# Milestone Progress

| Milestone | Status |
| --- | --- |
| 0. GitHub Repository & Environment Setup | IMPLEMENTED |
| 1. Dataset Feasibility & Graph Modeling | NOT STARTED |
| 2. Neo4j Setup & Data Ingestion | NOT STARTED |
| 3. FastAPI & Advanced Cypher | NOT STARTED |
| 4. Graph Analytics & Disruption Simulation | NOT STARTED |
| 5. Machine Learning Workflow | NOT STARTED |
| 6. AI Assistant & Guardrails | NOT STARTED |
| 7. Docker Integration, Testing & CI/CD | NOT STARTED |
| 8. Optimization, Documentation & Demo | NOT STARTED |

---

# Milestone 0 — Repository & Environment Setup

## Completed Work

- Installed and configured Git.
- Verified Python 3.13.3 installation.
- Created the local FlightGraph repository.
- Created the public GitHub repository.
- Configured `main` as the stable branch.
- Established a feature-branch workflow.
- Created and committed `.gitignore`.
- Created an initial README.
- Created `.env.example`.
- Configured an isolated Python virtual environment.
- Installed FastAPI, Uvicorn, and pytest.
- Created `requirements.txt`.
- Opened and merged the first Pull Request.
- Synchronized local `main` with GitHub.

## Remaining Verification

- Commit and merge the evaluation tracker.
- Verify the final repository structure.
- Confirm that the working tree is clean.
- Record Milestone 0 completion.

---

# Open Questions

## Solo Project Grading

The professor's rubric contains collaboration requirements originally
designed for teams.

Clarification is needed regarding:

1. Balanced commit contributions.
2. Code review requirements for a solo developer.
3. Substantial merged Pull Requests per member.
4. Whether solo self-reviews are accepted.

Do not fabricate contributors, reviews, or contribution statistics.

## Dataset and Architecture

The following decisions will be addressed in Milestone 1:

- Verify the structure and quality of the OpenFlights dataset.
- Compare alternative Neo4j graph schemas.
- Select appropriate airport and route identifiers.
- Define the disruption simulation methodology.
- Evaluate feasibility of the proposed ML workflow.
- Document the limitations of historical airline route data.

---

# Project Management Principles

1. Prioritize the professor's grading requirements.
2. Keep the implementation realistic within 40–50 hours.
3. Favor simple, maintainable architecture.
4. Implement and test functionality incrementally.
5. Use GitHub from the beginning.
6. Document technical decisions and trade-offs.
7. Never invent test results, benchmarks, or ML metrics.
8. Mark requirements VALIDATED only after verification.
9. Keep `main` stable.
10. Maintain an honest, professional GitHub portfolio.
