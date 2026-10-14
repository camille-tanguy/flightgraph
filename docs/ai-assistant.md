# Intent Validation and Security Guardrails

## LLM Intent Validation

The LLM interprets natural-language questions and returns a structured
intent containing an operation and airport parameters.

However, structured output alone does not guarantee that the
parameters are valid or sufficient.

FlightGraph therefore applies deterministic validation rules before
executing any database operation.

The validation layer ensures that:

- Only supported operations are accepted.
- Required airport parameters are provided.
- IATA codes contain exactly three alphabetical characters.
- Airport codes are normalized to uppercase.
- Unsupported requests cannot trigger database execution.

This separates LLM interpretation from application authorization.

The LLM proposes an action, but Python decides whether that action
is permitted.

## Service Orchestration

The assistant uses a dedicated service layer to coordinate
natural-language interpretation, intent validation, and database access.

The LLM returns a structured intent but does not execute database queries.

The application validates the intent and dispatches it to an explicitly
approved operation.

The initial implementation supports airport closure simulation by reusing
the existing `simulate_airport_closure()` service.

Additional supported operations will be integrated incrementally.

Automated tests use mocks to verify successful execution and rejection
of unsupported requests without external API calls.
