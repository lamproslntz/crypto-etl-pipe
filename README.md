# Crypto ETL Pipeline

## About the Project

The objective of this ETL pipeline is to enable market analysis, reporting and development of predictive modeling for cryptocurrency markets through an automated, consistent, scalable and accurate data collection process.

## Architecture

![Architecture](/images/architecture.png)
*Fig 1. ETL Pipelines in Ecosystems*

### ETL Pipeline Workflow

![Airflow DAG](/images/airflow_dag.png)
*Fig 2. Airflow ETL Pipeline*

* Airflow DAG Creation
  * A unique DAG is created for each cryptocurrency symbol. This modular approach allows for independent scheduling and execution of tasks related to each symbol.
* Scheduling
  * The pipeline is scheduled to run daily, ensuring the data is kept up to date with the latest open and close dates from Polygon.io.
  * Users define the start date for the pipeline. This date can be in the past, enabling the pipeline to backfill historical data.
* Catchup Mechanism
  * If the user-defined start date is in the past, Airflow's catchup feature is utilized to backfill data. The pipeline will execute tasks to extract historical information for the specified date range until it reaches the current date.

### Database

#### Crypto Prices Table

- crypto_symbol (character varying): Cryptocurrency symbol (e.g. BTC, DOGE, etc.).
- capture_date (date): The date at which open and close prices were requested.
- price_currency (character varying): Currency used for prices (e.g. USD, EUR, etc.).
- price_open (double precision): The open price for the symbol in the given time period.
- price_close (double precision): The close price for the symbol in the given time period.

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

  **Note: The ETL pipeline extracts information starting 2020-01-01 for BTC, ETH, DOGE and MATIC.**

11. (Optional) If port 8080 or 5432 are in use on your machine by other services, the Airflow webserver and metadata database won't be able to start. To run these components on different ports, run the following commands

  ```bash
  astro config set webserver.port <available-port>
  astro config set postgres.port <available-port>
  ```

12. Start Apache Airflow with Astro CLI

  ```bash
  astro dev start
  ```

13. Access Apache Airflow on your browser at [http://localhost:8080](http://localhost:8080).

## Extras

1. Stop Apache Airflow with Astro CLI

  ```bash
  astro dev stop
  ```

2. Restart Apache Airflow with Astro CLI

  ```bash
  astro dev restart
  ```

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
