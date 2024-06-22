from typing import Optional

import pendulum
from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from decouple import config

from include.configs import airflow_config
from include.crypto_etl.crypto_extract import crypto_extract
from include.crypto_etl.crypto_transform import crypto_transform

logger = airflow_config.task_log


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


@dag(
    dag_id="crypto_etl_pipe",
    default_args=airflow_config.default_args,
    start_date=pendulum.datetime(2020, 1, 1),
    schedule="@daily",
    template_searchpath="/usr/local/airflow/include/crypto_db/",
    catchup=False,
    description="ETL Pipeline for Crypto Data from Polygon",
    tags=["start", "setup"],
)
def crypto_pipeline():
    """ETL pipeline for crypto data from Crypto Polygon API."""
    drop_tables = SQLExecuteQueryOperator(
        task_id="drop_tables",
        conn_id="crypto_etl_pipe",
        sql="drop_tables.sql",
    )
    create_crypto_symbols_table = SQLExecuteQueryOperator(
        task_id="create_crypto_symbols_table",
        conn_id="crypto_etl_pipe",
        sql="create_crypto_symbols.sql",
    )
    create_crypto_prices_table = SQLExecuteQueryOperator(
        task_id="create_crypto_prices_table",
        conn_id="crypto_etl_pipe",
        sql="create_crypto_prices.sql",
    )

    raw_data = extract_task(polygon_api_key=config("POLYGON_API_KEY"))
    transformed_data = transform_task(response=raw_data)

    insert_crypto_prices = SQLExecuteQueryOperator(
        task_id="insert_crypto_prices",
        conn_id="crypto_etl_pipe",
        sql="insert_crypto_prices.sql",
        parameters={
            "crypto_symbol": "BTC",
            "capture_date": "2023-01-01",
            "price_currency": "USD",
            "price_open": 16532,
            "price_close": 16611.58,
        },  # TODO
    )

    chain(
        EmptyOperator(task_id="begin"),
        drop_tables,
        create_crypto_symbols_table,
        create_crypto_prices_table,
        raw_data,
        transformed_data,
        insert_crypto_prices,
        EmptyOperator(task_id="end"),
    )


crypto_pipeline()
