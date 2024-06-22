CREATE TABLE IF NOT EXISTS crypto_prices
(
	crypto_id bigint NOT NULL,
	capture_date date NOT NULL,
	price_currency character varying(255) NOT NULL,
	price_open money NOT NULL,
	price_close money NOT NULL,
	PRIMARY KEY (crypto_id, capture_date),
	FOREIGN KEY (crypto_id)
        REFERENCES crypto_symbols (crypto_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);