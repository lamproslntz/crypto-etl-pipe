CREATE TABLE IF NOT EXISTS crypto_symbols
(
	crypto_id bigserial NOT NULL,
	crypto_symbol character varying(255) NOT NULL,
	PRIMARY KEY (crypto_id)
);