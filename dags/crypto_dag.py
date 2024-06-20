from airflow.decorators import dag, task
from pendulum import datetime
from include.global_variables import airflow_config_variables as airflow_config

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
    print("Hello World!")


dag = crypto_pipeline()
