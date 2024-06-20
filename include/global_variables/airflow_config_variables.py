import logging
from pendulum import duration


# get Airflow task logger
task_log = logging.getLogger("airflow.task")


# DAG default arguments
default_args = {
    "retries": 1,
    "retry_delay": duration(minutes=1),
}
