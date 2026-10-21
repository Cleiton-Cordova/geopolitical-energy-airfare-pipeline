CREATE TABLE energy_airfare (
    date DATE NOT NULL,
    country_code VARCHAR(2) NOT NULL,
    country VARCHAR(50) NOT NULL,
    airfare_index NUMERIC(10, 2) NOT NULL,
    price_usd_per_barrel NUMERIC(10, 4) NOT NULL,
    price_usd_per_gallon NUMERIC(10, 4) NOT NULL,
    PRIMARY KEY (date, country_code)
);