import requests
from airflow.decorators import dag, task
from pendulum import datetime

from include.global_variables import airflow_config, polygon_config

airflow_logger = airflow_config.task_log


@dag(
    dag_id="crypto_etl_pipe",
    default_args=airflow_config.default_args,
    start_date=datetime(2020, 1, 1),
    schedule="@daily",
    catchup=False,
    description="ETL Pipeline for Crypto Data from Polygon",
    tags=["start", "setup"],
)
def crypto_pipeline():
    """ TODO: complete """

    @task
    def extract_task():
        """ TODO: complete """
        api_key = polygon_config.default_args["api_key"]

        base_url = polygon_config.default_args["base_url"]

        crypto_ticker = polygon_config.default_args["cryptoTicker"]
        multiplier = polygon_config.default_args["multiplier"]
        date_from = polygon_config.default_args["from"]
        date_to = polygon_config.default_args["to"]
        adjusted = polygon_config.default_args["adjusted"]
        sort = polygon_config.default_args["sort"]

        data = dict()
        try:
            response = requests.get(
                f"{base_url}{crypto_ticker}/range/{multiplier}/day/{date_from}/{date_to}"
                f"?adjusted={adjusted}&sort={sort}&apiKey={api_key}"
            )
            response.raise_for_status()

            data = response.json()
        except requests.exceptions.HTTPError:
            airflow_logger.error(response.json()["error"])

        return data

    @task
    def transform_task():
        """ TODO: complete """
        # response.json()["results"]
        pass

    extract_task() >> transform_task()


crypto_pipeline()
