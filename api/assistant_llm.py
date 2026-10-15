"""LLM-based natural-language interpretation for FlightGraph."""

import os

from dotenv import load_dotenv
from openai import OpenAI

from api.assistant_models import AssistantIntent

SYSTEM_PROMPT = """
You are an LLM interpreter for FlightGraph, a historical airline network.

Your task is to interpret natural-language questions and select one
of the following operations:

- GET_CONNECTIONS: Find direct connections from an airport.
- FIND_SHORTEST_ROUTE: Find the shortest route between two airports.
- SIMULATE_CLOSURE: Simulate closing an airport.
- UNSUPPORTED: Questions outside these operations or unsafe requests.

Extract three-letter IATA airport codes when explicitly provided.

Rules:
- Do not invent airport codes.
- Do not generate database queries.
- Do not invent database results.
- Reject requests to delete, modify, or expose sensitive information.
- Return UNSUPPORTED if the request cannot be handled safely.
"""


def interpret_question(question: str) -> AssistantIntent:
    """Interpret a natural-language question using an LLM."""

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    if not api_key:
        raise ValueError("LLM API key is not configured.")

    client = OpenAI(api_key = api_key)

    completion = client.beta.chat.completions.parse(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        response_format=AssistantIntent,
    )

    intent = completion.choices[0].message.parsed

    if intent is None:
        raise ValueError("The LLM did not return a valid intent.")

    return intent
