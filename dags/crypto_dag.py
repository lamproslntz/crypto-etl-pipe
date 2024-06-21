import pendulum
import requests
from airflow.decorators import dag, task

from include.global_variables import airflow_config, polygon_config

airflow_logger = airflow_config.task_log


@dag(
    dag_id="crypto_etl_pipe",
    default_args=airflow_config.default_args,
    start_date=pendulum.datetime(2020, 1, 1),
    schedule="@daily",
    catchup=False,
    description="ETL Pipeline for Crypto Data from Polygon",
    tags=["start", "setup"],
)
def crypto_pipeline():
    """TODO: complete"""

    @task
    def extract_task():
        """TODO: complete"""
        # load Polygon API configurations
        api_key = polygon_config.default_args["api_key"]
        base_url = polygon_config.default_args["base_url"]
        symbol_from = polygon_config.default_args["symbol_from"]
        symbol_to = polygon_config.default_args["symbol_to"]
        date_capture = polygon_config.default_args["date_capture"]
        price_adjusted = polygon_config.default_args["price_adjusted"]

        data = dict()
        try:
            response = requests.get(
                f"{base_url}/{symbol_from}/{symbol_to}/{date_capture}?adjusted={price_adjusted}&apiKey={api_key}"
            )
            response.raise_for_status()

            data = response.json()
        except requests.exceptions.HTTPError:
            airflow_logger.error(response.json()["error"])

        return data

    @task
    def transform_task(data):
        """TODO: complete"""
        symbol, currency = data["symbol"].split("-")

        date_capture = pendulum.parse(data["day"])
        date_capture = date_capture.to_date_string()

        # default values
        crypto_info = {
            "symbol": symbol,
            "currency": currency,
            "day": date_capture,
            "open_price": data["open"],
            "close_price": data["close"],
        }

        return crypto_info

    transform_task(extract_task())
    # transformed_data = transform_task(extract_task())
    # extract_task() >> transform_task()


crypto_pipeline()
