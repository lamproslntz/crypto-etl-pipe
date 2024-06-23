import logging
from typing import Optional

import pendulum
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from decouple import config

from include.crypto_db.create_table import create_crypto_prices_table
from include.crypto_etl.crypto_extract import crypto_extract
from include.crypto_etl.crypto_load import crypto_load
from include.crypto_etl.crypto_transform import crypto_transform

logger = logging.getLogger("airflow.task")


@task(task_id="setup_db_tables")
def setup_task(postgres_conn_id: str) -> None:
    """Task for setting up the database schema (tables, sequences, etc.).

    Args:
        postgres_conn_id:
            The postgres conn id reference to a specific postgres database.
    """
    create_crypto_prices_table(postgres_conn_id=postgres_conn_id)


@task(task_id="extract")
def extract_task(polygon_api_key: str, **context) -> Optional[dict]:
    """Task for extracting open and close prices of a crypto symbol on a certain day using Crypto Polygon API.

    Args:
        polygon_api_key:
            Polygon API key.

    Returns:
        Open and close prices of a crypto symbol on a certain day, otherwise None.
        See Crypto Polygon API documentation [here](https://polygon.io/docs/crypto/getting-started).
    """
    capture_date = context["ds"]
    response = crypto_extract(polygon_api_key, capture_date=capture_date)

    # if Polygon API failed then retry
    if response is None:
        raise Exception(f"Polygon request for {capture_date} failed. Retrying ...")

    return response


@task(task_id="transform")
def transform_task(response: Optional[dict]) -> Optional[dict]:
    """Task for transformating Crypto Polygon API data.

    Args:
        response:
            Crypto Polygon API response.

    Returns:
        Tranformed Crypto Polygon API data, otherwise None.

        {
            'crypto_symbol': 'BTC',
            'price_currency': 'USD',
            'date_capture': "2023-01-01",
            'price_open': 16532,
            'price_close': 16611.58,
        }
    """
    return crypto_transform(response)


@task(task_id="load")
def load_task(postgres_conn_id: str, records: Optional[dict]) -> None:
    """Task for uploading transformed data from Crypto Polygon API.

    Args:
        postgres_conn_id:
            The postgres conn id reference to a specific postgres database.
        records:
            Tranformed Crypto Polygon API data.
    """
    crypto_load(postgres_conn_id, records)


@dag(
    dag_id="crypto_etl_pipe",
    start_date=pendulum.datetime(2024, 6, 1),
    schedule="@daily",
    catchup=True,
    default_args={
        "retries": 5,
        "retry_delay": pendulum.duration(minutes=1),
        "depends_on_past": False,
    },
    description="ETL pipeline for crypto data from Polygon",
    tags=["polygon", "crypto"],
)
def crypto_pipeline():
    """ETL pipeline for crypto data from Crypto Polygon API."""
    begin_task = EmptyOperator(task_id="begin")
    end_task = EmptyOperator(task_id="end")

    setup_db_tables = setup_task(postgres_conn_id="crypto_etl_pipe")

    raw_data = extract_task(polygon_api_key=config("POLYGON_API_KEY"))
    transformed_data = transform_task(response=raw_data)
    loaded_data = load_task(
        postgres_conn_id="crypto_etl_pipe", records=transformed_data
    )

    begin_task >> setup_db_tables >> loaded_data
    begin_task >> raw_data >> transformed_data >> loaded_data >> end_task


crypto_pipeline()
