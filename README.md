# Crypto ETL Pipeline

## About the Project

TODO:

## Architecture

### ETL Pipeline

TODO:

### Database

TODO:

## What You Need

1. Docker and Docker Compose (see [here](https://www.docker.com/products/docker-desktop/)).

2. Astro CLI to run Apache Airflow (see [here](https://www.astronomer.io/docs/astro/cli/install-cli)).

3. PostgreSQL (see [here](https://www.postgresql.org/download/)).

4. Polygon acount and API key (see [here](https://polygon.io/)).

5. Clone the repository.

  ```bash
  git clone https://github.com/lamproslntz/crypto-etl-pipe.git
  ```

6. Change into the project directory.

  ```bash
  cd crypto-etl-pipe
  ```

7. Create a PostgreSQL database to host the data.

  ```sql
  CREATE DATABASE <your-database-name>
    WITH
    ENCODING = 'UTF8';
  ```

8. Create a .env (see [.env.sample](.env.sample)) and save your Polygon API key.

9. Create a airflow_settings.yaml (see [airflow_settings.yaml.sample](airflow_settings.yaml.sample)) and save your PostgreSQL database information.

10. (Optional) Modify the Airflow DAG settings (see [/dags/dags_settings.py](/dags/dags_settings.py)).

11. (Optional) If port 8080 or 5432 are in use on your machine by other services, the Airflow webserver and metadata database won't be able to start. To run these components on different ports, run the following commands

  ```bash
  astro config set webserver.port <available-port>
  astro config set postgres.port <available-port>
  ```

12. Start Apache Airflow with Astro CLI

  ```bash
  astro dev start
  ```

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
