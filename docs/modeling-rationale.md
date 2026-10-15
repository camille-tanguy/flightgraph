# FlightGraph — Modeling Rationale and Anti-Genericity Analysis

## 1. Modeling Objective

FlightGraph models historical airline connections to support airport
exploration, shortest-path analysis, graph centrality, and disruption
simulation.

The graph is designed around the project's research question:

> How can graph analytics and AI identify critical airports, evaluate
> network disruptions, and recommend alternative connections?

The primary analytical entities are airports and their directed
connections, rather than individual scheduled flights.

The dataset comes from OpenFlights, which provides historical airport
and route information rather than live airline schedules.

The database schema is therefore designed for network analysis,
not operational airline management.

## 2. Modeling Alternatives Considered

Two main approaches were evaluated.

### Alternative A — Direct Airport-to-Airport Relationships

In this model, each historical airport connection is represented
by a directed relationship.

```text
(Airport)-[:FLIES_TO]->(Airport)
```

A relationship represents the existence of a recorded connection
from one airport to another.

**Advantages:**

- Simple airport-to-airport traversal.
- Straightforward shortest-path and multi-hop reachability queries.
- Direct compatibility with graph analytics.
- Efficient creation of airport-only GDS projections.
- Simple exclusion of airports during disruption simulations.

**Limitations:**

- Individual airline services are aggregated.
- Airline-specific analysis requires inspecting relationship properties.
- Flight schedules and frequencies are not represented.
- Multiple route records between the same airport pair are not
  preserved as separate relationships.

This approach is appropriate when the primary objective is to
analyze network structure rather than individual flight operations.

### Alternative B — Separate Route Nodes

An alternative would represent each route as a separate node.

```text
(Airport)-[:ORIGIN_OF]->(Route)-[:DESTINATION]->(Airport)
```

Each `Route` node could store information such as:

- Origin and destination airport identifiers.
- Operating airline.
- Number of stops.
- Aircraft information, where available.

**Advantages:**

- Preserves more route-level detail.
- Allows individual routes to have independent properties.
- Supports more detailed airline-specific analysis.
- Offers greater flexibility for future operational extensions.

**Limitations:**

- Requires additional nodes and relationships.
- Makes airport-to-airport traversal less direct.
- Requires additional transformations for airport-only graph analytics.
- Introduces complexity that does not directly improve
  FlightGraph's principal disruption simulation.

This alternative would be more appropriate for an application
focused on detailed airline operations or route-level analysis.

### Comparison

| Criterion | Direct `FLIES_TO` relationships | Separate `Route` nodes |
| --- | --- | --- |
| Airport-to-airport traversal | Direct | Requires additional relationships |
| Shortest-path queries | Straightforward | More complex |
| PageRank and WCC | Direct airport graph projection | Additional projection logic |
| Airline-specific route details | Aggregated | More flexible |
| Historical route record preservation | Limited | More detailed |
| Airport closure simulation | Simple airport exclusion | More complex relationship handling |
| Fit for FlightGraph | High | Lower for current scope |

Neither model is universally superior.

The appropriate choice depends on the research question,
available data, and intended graph operations.

## 3. Selected Graph Model

FlightGraph adopts direct, directed `FLIES_TO` relationships
between `Airport` nodes.

The implemented graph contains three node labels:

- `Airport`
- `Airline`
- `Country`

And three relationship types:

- `FLIES_TO`
- `OPERATES`
- `LOCATED_IN`

### 3.1 Airport Nodes

Airport nodes store information including:

- `airport_id`
- `name`
- `city`
- `country`
- `iata`
- `latitude`
- `longitude`

Each airport is uniquely identified by its OpenFlights `airport_id`.

IATA codes are indexed for efficient airport lookups but are
not assumed to be globally unique in the original dataset.

This distinction matters because using IATA as the unique
identifier could incorrectly merge airport records.

### 3.2 Directed Flight Connections

Flight connections use the following representation:

```text
(Airport)-[:FLIES_TO]->(Airport)
```

Direction is preserved because a recorded route from airport A
to airport B does not necessarily imply a recorded route from
airport B to airport A.

Directed relationships support:

- Direct connection exploration.
- Shortest-path analysis.
- Multi-hop reachability.
- PageRank.
- Weakly Connected Components.
- Airport closure simulations.

FlightGraph aggregates multiple airlines serving the same
directed airport pair.

For example:

```text
(Airport A)-[:FLIES_TO {
    airlines: ["AF", "DL"],
    airline_count: 2
}]->(Airport B)
```

This reduces unnecessary duplication in the network used
for graph analytics.

However, it means that individual route records are no
longer represented separately.

### 3.3 Airline Nodes

Airlines are represented as separate nodes:

```text
(Airline)-[:OPERATES]->(Airport)
```

The `OPERATES` relationship indicates that an airline serves
an airport within the historical dataset.

It does not represent an individual flight or specify
a particular route direction.

Airline codes are protected by a uniqueness constraint.

### 3.4 Country Nodes

Airports are connected to countries through:

```text
(Airport)-[:LOCATED_IN]->(Country)
```

This allows airports to share a common country entity.

Countries are identified by their name, with a uniqueness
constraint preventing duplicate country nodes with the same
name.

## 4. Why This Model Fits FlightGraph

The schema was selected based on three engineering considerations.

### 4.1 Alignment with the Research Question

FlightGraph evaluates the structural resilience of an
airline network.

Its main questions concern:

- Which airports are structurally influential?
- Which airports are reachable from a given origin?
- How does removing an airport affect connectivity?
- Which connections remain after a disruption?

These questions primarily involve airports and the
connections between them.

Creating separate entities for every route record would
add complexity without directly improving these analyses.

### 4.2 Compatibility with Graph Algorithms

FlightGraph implements graph analytics through
Neo4j Graph Data Science.

Its airport-only projection contains:

- **7,698 airport nodes**
- **36,906 directed airport-to-airport relationships**

Two graph algorithms are used:

**PageRank*

PageRank measures structural influence based on the
network's directed connections.

It can help identify airports that occupy influential
positions within the historical network.

However, a high PageRank score does not automatically
imply that closing an airport would cause severe fragmentation.

**Weakly Connected Components (WCC)*

WCC identifies groups of airports connected when
relationship direction is ignored.

FlightGraph uses WCC to compare network connectivity
before and after an airport closure.

Because the main analytical graph already consists of
direct airport connections, these algorithms can operate
without traversing separate route entities.

### 4.3 Simplicity and Maintainability

FlightGraph is developed as a solo software engineering project
with a limited implementation budget.

The selected model makes it easier to:

- Maintain a clear database schema.
- Implement and test graph queries.
- Construct GDS projections.
- Simulate airport closures.
- Explain results to users.
- Document architectural decisions.

The design prioritizes a reliable and maintainable application
over unnecessary schema complexity.

## 5. Anti-Genericity Analysis

A generic airline database might include entities such as:

- Airport
- Airline
- Aircraft
- Flight
- Route
- Passenger
- Booking

Such a model could support reservations, scheduling,
passenger management, and airline operations.

FlightGraph deliberately does not model those activities.

Instead, its schema is specialized for network resilience.

### 5.1 Airports as Units of Disruption

The disruption simulator removes an airport from a
temporary graph projection and measures the consequences
for network connectivity.

This directly reflects the application's principal feature:
airport closure simulation.

### 5.2 Connections as Graph Relationships

Historical connections are represented as direct
`FLIES_TO` relationships because FlightGraph frequently
performs airport-to-airport traversals.

This makes the principal analytical operations
straightforward to express in Cypher and GDS.

### 5.3 Aggregated Airline Information

Airline information is aggregated on airport connections
instead of generating separate route entities for
every airline service.

This is a deliberate trade-off.

The application preserves information about which airlines
serve a connection while prioritizing network-level analysis.

### 5.4 Specialized Graph Analytics

The graph model directly supports:

- PageRank for structural influence.
- Weakly Connected Components for fragmentation analysis.
- Shortest-path and reachability queries.
- Temporary airport-exclusion projections.

The database structure therefore reflects the algorithms
and analytical questions implemented in FlightGraph.

### 5.5 Avoiding Unsupported Complexity

FlightGraph does not introduce entities such as
`Booking`, `Passenger`, or `FlightSchedule` because the
dataset does not provide the information required to
implement those concepts meaningfully.

Adding such entities would make the schema appear more
comprehensive without improving the validity of the
analysis.

The resulting model is intentionally narrower than a
general-purpose airline database.

## 6. Trade-offs and Limitations

The selected schema has several limitations.

### 6.1 Historical Data

OpenFlights contains historical route information.

The graph should not be interpreted as representing
currently available flights or active airline schedules.

### 6.2 No Operational Flight Information

The database does not contain reliable information about:

- Departure and arrival times.
- Ticket prices.
- Passenger demand.
- Seat capacity.
- Flight frequencies.
- Real-time cancellations.

Therefore, FlightGraph cannot estimate the complete
operational or economic consequences of airport closures.

### 6.3 Aggregated Routes

Aggregating airlines by directed airport pair simplifies
network analysis.

However, it reduces flexibility for detailed
airline-specific comparisons.

A future project requiring richer route-level analysis
might benefit from separate route entities.

### 6.4 Graph Connectivity Is Not Operational Reachability

Graph connectivity does not guarantee that a real
passenger could complete an itinerary.

For example, WCC ignores relationship direction.

Likewise, a shortest path based on the number of
connections does not account for schedules,
connection times, airline restrictions, or cost.

### 6.5 Structural Importance Versus Disruption Impact

PageRank identifies structurally influential airports,
but its scores should not be interpreted directly as
predictions of disruption severity.

The disruption simulator measures the consequences
of a specific airport closure using connectivity metrics.

These are complementary but distinct analytical approaches.

## 7. Conclusion

FlightGraph's graph schema represents a deliberate
trade-off between analytical usefulness,
implementation complexity, and data availability.

Direct airport-to-airport relationships were selected
because they support the application's main operations:
graph traversal, centrality analysis, connectivity
measurement, and airport closure simulation.

Separate Airline and Country nodes preserve useful
information without complicating the principal
airport network.

The resulting schema is driven by FlightGraph's
research question rather than by a generic
airline database template.

## 8. Related Documentation

For the implemented node labels, relationships,
constraints, indexes, and GDS projection, see:

- [Graph Database Schema](graph-schema.md)
- [System Architecture](architecture.md)
- [Query Optimization](query-optimization.md)
