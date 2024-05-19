
CREATE SCHEMA IF NOT EXISTS assignement;

CREATE TABLE IF NOT EXISTS assignement.crypto_prices
(
	ticker VARCHAR(4),
	market_date DATE,
	price FLOAT,
	open_price FLOAT,
	high FLOAT,
	low FLOAT,
	volume VARCHAR(10),
	change VARCHAR(10),
	market_cap DECIMAL(20,2),
	circulating_supply DECIMAL(20,2),
	percent_change_24h VARCHAR(10),
	percent_change_7d DECIMAL(20,2)
);

COPY assignement.crypto_prices (ticker, market_date, price, open_price, high,low, volume, change, market_cap, circulating_supply, percent_change_24h, percent_change_7d)
FROM '/data/fake_crypto_data.csv' DELIMITER ',' CSV HEADER;