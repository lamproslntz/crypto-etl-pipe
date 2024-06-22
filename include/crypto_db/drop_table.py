from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging


logger = logging.getLogger(__package__)


def drop_table(postgres_conn_id: str, table: str) -> None:
    """Drops postgres table.
    
    Args:
        postgres_conn_id:
            The postgres conn id reference to a specific postgres database.
        table:
            Postgres table name.
    """
    try:
        with PostgresHook(postgres_conn_id).get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                        DROP TABLE IF EXISTS {table};
                    """
                )
    except Exception as e:
        logger.exception(f"Could not drop {table} table.")