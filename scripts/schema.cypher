// Unique airport identifiers.
CREATE CONSTRAINT airport_id_unique IF NOT EXISTS
FOR (a:Airport)
REQUIRE a.airport_id IS UNIQUE;

// Unique airline codes.
CREATE CONSTRAINT airline_code_unique IF NOT EXISTS
FOR (a:Airline)
REQUIRE a.code IS UNIQUE;

// Unique country names.
CREATE CONSTRAINT country_name_unique IF NOT EXISTS
FOR (c:Country)
REQUIRE c.name IS UNIQUE;

// Index for airport searches by IATA code.
CREATE INDEX airport_iata_index IF NOT EXISTS
FOR (a:Airport)
ON (a.iata);