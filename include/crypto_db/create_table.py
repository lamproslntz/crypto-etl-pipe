import logging

from airflow.providers.postgres.hooks.postgres import PostgresHook

logger = logging.getLogger(__package__)


def create_crypto_prices_table(postgres_conn_id: str) -> None:
    """Created crypto_prices postgres table.

    Args:
        postgres_conn_id:
            The postgres conn id reference to a specific postgres database.
    """
    try:
        with PostgresHook(postgres_conn_id).get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS crypto_prices
                        (
                            crypto_symbol character varying(255) NOT NULL,
                            capture_date date NOT NULL,
                            price_currency character varying(255) NOT NULL,
                            price_open double precision NOT NULL,
                            price_close double precision NOT NULL,
                            PRIMARY KEY (crypto_symbol, capture_date)
                        );
                    """
                )
    except Exception:
        logger.exception("Could not create crypto_prices table.")
