CREATE TABLE IF NOT EXISTS crypto_prices
(
	crypto_symbol character varying(255) NOT NULL,
	capture_date date NOT NULL,
	price_currency character varying(255) NOT NULL,
	price_open money NOT NULL,
	price_close money NOT NULL,
	PRIMARY KEY (crypto_symbol, capture_date)
);
