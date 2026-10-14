"""Pydantic models for FlightGraph API responses."""

from pydantic import BaseModel, Field


class AirportResponse(BaseModel):
    """Structured response containing airport information."""

    airport_id: int = Field(
        description="Unique OpenFlights airport ID"
    )
    name: str = Field(
        description="Airport name"
    )
    city: str | None = Field(
        description="City where the airport is located"
    )
    country: str = Field(
        description="Airport country"
    )
    iata: str = Field(
        description="Three-letter IATA airport code"
    )


class ConnectionResponse(BaseModel):
    """Structured response containing a direct flight connection."""

    iata: str | None = Field(
        description="Destination airport IATA code"
    )
    name: str = Field(
        description="Destination airport name"
    )
    city: str | None = Field(
        description="Destination airport city"
    )
    airline_count: int = Field(
        ge=1,
        description="Number of airlines serving this connection"
    )


class ShortestPathResponse(BaseModel):
    """Response containing the shortest route between two airports."""

    airports: list[str] = Field(
        description="Airport codes along the shortest path"
    )
    flights: int = Field(
        ge=0,
        description="Minimum number of flights required"
    )

class ReachableAirportResponse(BaseModel):
    """An airport reachable within a limited number of flights."""

    iata: str | None = Field(
        description="Destination airport IATA code"
    )
    name: str = Field(
        description="Destination airport name"
    )
    hops: int = Field(
        ge=1,
        description="Minimum number of flights required"
    )