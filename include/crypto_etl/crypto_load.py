from typing import Optional

from airflow.providers.postgres.hooks.postgres import PostgresHook


def crypto_load(postgres_conn_id: str, records: Optional[dict]) -> None:
    """Uploads transformed data from Crypto Polygon API.

    Args:
        postgres_conn_id:
            The postgres conn id reference to a specific postgres database.
        records:
            Tranformed Crypto Polygon API data.
    """
    if records is None:
        return None

    with PostgresHook(postgres_conn_id).get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"""
                    INSERT INTO crypto_prices
                    (
                        crypto_symbol,
                        capture_date,
                        price_currency,
                        price_open,
                        price_close
                    )
                        VALUES
                            (
                                '{records["crypto_symbol"]}',
                                '{records["date_capture"]}',
                                '{records["price_currency"]}',
                                {records["price_open"]},
                                {records["price_close"]}
                            )
                        ON CONFLICT DO NOTHING;
                """
            )
