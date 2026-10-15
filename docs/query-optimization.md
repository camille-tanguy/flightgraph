# Neo4j Query Performance Analysis

## Objective

This document evaluates the execution plans of selected FlightGraph
Cypher queries using Neo4j's `EXPLAIN` and `PROFILE` commands.

The objective is to verify index utilization, examine graph traversal
operations, and identify potential performance bottlenecks.

## Environment

- Database: Neo4j 5.26
- Runtime: SLOTTED
- Planner: COST
- Dataset: Historical OpenFlights
- Airports: 7,698
- Directed airport connections: 36,906

## 1. Airport Lookup

### Query

```cypher
PROFILE
MATCH (a:Airport {iata: "CDG"})
RETURN a.name, a.city, a.country;
```

### Execution Plan

Neo4j uses the following operators:

1. NodeIndexSeek
2. CacheProperties
3. Projection
4. ProduceResults

The `NodeIndexSeek` operator uses the range index on `Airport(iata)`.

### Measurements

| Metric | Result |
| --- | ---: |
| Rows returned | 1 |
| Total DB Hits | 5 |
| Allocated memory | 64 bytes |
| Index used | Airport(iata) |

### Interpretation

The database uses an index to locate the airport rather than
performing a full label scan.

No additional optimization was identified as necessary for this query.

## 2. Direct Airport Connections

 Query

```cypher
PROFILE
MATCH (source:Airport {iata: "CDG"})
      -[:FLIES_TO]->
      (destination:Airport)
RETURN destination.iata AS destination
LIMIT 10;
```

 Execution Plan

Neo4j uses the following operators:

1. NodeIndexSeek
2. Expand(All)
3. Filter
4. Limit
5. Projection
6. ProduceResults

The source airport is located using `Airport(iata)`.
Neo4j then follows outgoing `FLIES_TO` relationships.

 Measurements

| Metric | Result |
| --- | ---: |
| Rows returned | 10 |
| Total DB Hits | 37 |
| Allocated memory | 64 bytes |
| Index used | Airport(iata) |

 Interpretation

The query performs an indexed airport lookup followed by directed
relationship traversal.

No full airport scan was observed.

The execution plan does not indicate an obvious performance bottleneck.

Because the query uses `LIMIT 10` without `ORDER BY`, the specific
destinations returned are not guaranteed to be consistent.

## 3. Summary

| Metric | Airport Lookup | Direct Connections |
| --- | ---: | ---: |
| Index used | Yes | Yes |
| Graph traversal | No | Yes |
| Rows returned | 1 | 10 |
| Total DB Hits | 5 | 37 |
| Full airport scan | No | No |

Both queries use index-based starting points.

The direct-connections query performs additional database accesses
because it traverses relationships and retrieves destination properties.

The two DB Hit counts are not directly comparable as performance
benchmarks because the queries perform different operations.

## 4. Limitations

- `EXPLAIN` displays the planned execution without executing the query.
- `PROFILE` executes the query and reports actual operator statistics.
- DB Hits measure logical database accesses, not elapsed execution time.
- These measurements were collected from individual executions.
- Execution times were not benchmarked across repeated runs.
- Query performance may vary with database size, caching, and hardware.

## 5. Conclusion

The analyzed FlightGraph queries use the existing airport IATA index
and avoid unnecessary full airport scans.

The results demonstrate appropriate index utilization and directed
graph traversal.

No performance modification was justified by these two execution plans.
