import logging
from typing import Optional

import pendulum
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from dags_settings import dags_settings
from decouple import config

from include.crypto_db.create_table import create_crypto_prices_table
from include.crypto_etl.crypto_extract import crypto_extract
from include.crypto_etl.crypto_load import crypto_load
from include.crypto_etl.crypto_transform import crypto_transform

logger = logging.getLogger("airflow.task")


CRYPTOCURRENCIES = dags_settings["crypto"]["cryptos"]
START_DATE = dags_settings["crypto"]["start_date"]
RETRIES = dags_settings["crypto"]["retries"]


@task(task_id="setup_db_tables")
def setup_task(postgres_conn_id: str) -> None:
    """Task for setting up the database schema (tables, sequences, etc.).

    Args:
        postgres_conn_id:
            The postgres conn id reference to a specific postgres database.
    """
    create_crypto_prices_table(postgres_conn_id=postgres_conn_id)


@task(task_id="extract")
def extract_task(crypto_symbol: str, polygon_api_key: str, **context) -> Optional[dict]:
    """Task for extracting open and close prices of a crypto symbol on a certain day using Crypto Polygon API.

    Args:
        crypto_symbol:
            Crypto symbol (e.g. BTC, DOGE, etc.).
        polygon_api_key:
            Polygon API key.

    Returns:
        Open and close prices of a crypto symbol on a certain day, otherwise None.
        See Crypto Polygon API documentation [here](https://polygon.io/docs/crypto/getting-started).
    """
    capture_date = context["ds"]
    response = crypto_extract(
        crypto_symbol=crypto_symbol,
        capture_date=capture_date,
        polygon_api_key=polygon_api_key,
    )

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


def create_dag(dag_id: str, crypto_symbol: str):
    """Creates Aiflow DAGs representing ETL pipelines for crypto data from Crypto Polygon API.

    Args:
        dag_id:
            Aiflow DAG identifier.
        crypto_symbol:
            Crypto symbol (e.g. BTC, DOGE, etc.).
    """

    @dag(
        dag_id=dag_id,
        start_date=pendulum.parse(START_DATE),
        schedule="@daily",
        catchup=True,
        default_args={
            "retries": 80,
            "retry_delay": pendulum.duration(minutes=1),
            "depends_on_past": False,
        },
        tags=["polygon", "crypto", crypto_symbol],
    )
    def crypto_pipeline():
        """ETL pipeline for crypto data from Crypto Polygon API."""
        begin_task = EmptyOperator(task_id="begin")
        end_task = EmptyOperator(task_id="end")

        setup_db_tables = setup_task(postgres_conn_id="crypto_etl_pipe")

        raw_data = extract_task(
            crypto_symbol=crypto_symbol, polygon_api_key=config("POLYGON_API_KEY")
        )
        transformed_data = transform_task(response=raw_data)
        loaded_data = load_task(
            postgres_conn_id="crypto_etl_pipe", records=transformed_data
        )

        begin_task >> setup_db_tables >> loaded_data
        begin_task >> raw_data >> transformed_data >> loaded_data >> end_task

    return crypto_pipeline()


for crypto in CRYPTOCURRENCIES:
    dag_id = f"{crypto.lower()}_etl_pipe"

    globals()[dag_id] = create_dag(dag_id=dag_id, crypto_symbol=crypto)
