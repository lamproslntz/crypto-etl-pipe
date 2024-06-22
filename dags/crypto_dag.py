from typing import List, Optional

import pendulum
from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from decouple import config

from include.configs import airflow_config
from include.crypto_db.create_table import create_crypto_prices_table
from include.crypto_db.drop_table import drop_table
from include.crypto_etl.crypto_extract import crypto_extract
from include.crypto_etl.crypto_load import crypto_load
from include.crypto_etl.crypto_transform import crypto_transform

logger = airflow_config.task_log


@task
def reset_task(postgres_conn_id: str, tables: List[str]) -> None:
    """Task for reseting postgres tables.

    Args:
        postgres_conn_id:
            The postgres conn id reference to a specific postgres database.
        tables:
            List of postgres tables.
    """
    for table in tables:
        drop_table(postgres_conn_id=postgres_conn_id, table=table)


@task
def setup_task(postgres_conn_id: str) -> None:
    """Task for setting up the database schema (tables, sequences, etc.).

    Args:
        postgres_conn_id:
            The postgres conn id reference to a specific postgres database.
    """
    create_crypto_prices_table(postgres_conn_id=postgres_conn_id)


@task
def extract_task(polygon_api_key: str) -> Optional[dict]:
    """Task for extracting open and close prices of a crypto symbol on a certain day using Crypto Polygon API.

    Args:
        polygon_api_key:
            Polygon API key.

    Returns:
        Open and close prices of a crypto symbol on a certain day, otherwise None.
        See Crypto Polygon API documentation [here](https://polygon.io/docs/crypto/getting-started).
    """
    return crypto_extract(polygon_api_key)


@task
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


@task
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
    default_args=airflow_config.default_args,
    start_date=pendulum.datetime(2020, 1, 1),
    schedule="@daily",
    catchup=False,
    description="ETL Pipeline for Crypto Data from Polygon",
    tags=["polygon", "crypto"],
)
def crypto_pipeline():
    """ETL pipeline for crypto data from Crypto Polygon API."""
    chain(
        EmptyOperator(
            task_id="begin",
        ),
        reset_task(
            postgres_conn_id="crypto_etl_pipe",
            tables=["crypto_prices"],
        ),
        setup_task(
            postgres_conn_id="crypto_etl_pipe",
        ),
        load_task(
            postgres_conn_id="crypto_etl_pipe",
            records=transform_task(
                response=extract_task(polygon_api_key=config("POLYGON_API_KEY")),
            ),
        ),
        EmptyOperator(
            task_id="end",
        ),
    )


crypto_pipeline()
