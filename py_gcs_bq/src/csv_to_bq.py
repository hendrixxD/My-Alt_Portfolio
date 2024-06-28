"""
Loads a CSV file from local machine to BigQuery.
"""

import os
import logging
from google.cloud import bigquery
import pandas as pd


class BigQueryTransmiter:
    """
    Initializing BigQueryTransmiter with the project details and CSV file path.
    """
    def __init__(self, project_id, dataset_id, table_id, csv_filepath):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.csv_filepath = csv_filepath
        self.client = bigquery.Client()

        # logger for BigQueryTransmiter
        self.logger = logging.getLogger(f"{__name__}.BigQueryTransmiter")
        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            fh = logging.FileHandler("bigquerytransmiter.log")
            fh.setLevel(logging.INFO)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)
    

    # adds a new line to the log files before execution for readability
    def log_newline(self):
        self.logger.info("\n")


    def validate_dataset_existence(self):
        """
        Check if the dataset exists in BigQuery, else, it creates it.
        """
        dataset_ref = bigquery.DatasetReference(self.project_id, self.dataset_id)

        try:
            self.client.get_dataset(dataset_ref)
            self.logger.info(f"Dataset `{self.dataset_id}` already exists.")
        except Exception:
            # Creates a dataset if it doesn't exist
            self.logger.info(f"Dataset `{self.dataset_id}` does not exist. Creating a dataset.")
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "europe-west1"

            self.client.create_dataset(dataset)
            self.logger.info(f"Dataset `{self.dataset_id}` created.")


    def csv_to_dataframe(self):
        """
        Loads the CSV file to a pandas DataFrame.
        """
        self.logger.info("Starting to load CSV file...")

        if not os.path.exists(self.csv_filepath):
            self.logger.error(f"{self.csv_filepath}: not found!")
            raise FileNotFoundError(f"{self.csv_filepath}: not found!")

        self.dataframe = pd.read_csv(self.csv_filepath)
        self.logger.info(f"Successfully loaded CSV file into DataFrame with {len(self.dataframe)} rows")


    def transmit_to_bigquery(self):
        """
        The DataFrame is uploaded to BigQuery.
        Idempotency is ensured by truncating the table if it exists already upon execution.
        """
        self.logger.info("Starting to upload to BigQuery...")
        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

        # bq schema
        schema = [
            bigquery.SchemaField("ticker", "STRING"),
            bigquery.SchemaField("market_date", "DATE"),
            bigquery.SchemaField("change", "FLOAT"),
            bigquery.SchemaField("price", "FLOAT"),
            bigquery.SchemaField("open_price", "FLOAT"),
            bigquery.SchemaField("high", "FLOAT"),
            bigquery.SchemaField("low", "FLOAT"),
            bigquery.SchemaField("volume", "STRING"),
            bigquery.SchemaField("change", "STRING"),
            bigquery.SchemaField("market_cap", "NUMERIC"),
            bigquery.SchemaField("circulating_supply", "BIGNUMERIC"),
            bigquery.SchemaField("percent_change_24h", "STRING"),
            bigquery.SchemaField("percent_change_7d", "FLOAT64")
        ]

        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.CSV
        )

        try:
            load_job = self.client.load_table_from_dataframe(
                self.dataframe,
                table_ref,
                job_config=job_config
            )

            load_job.result()

            table = self.client.get_table(table_ref)

            self.logger.info(f"Loaded {table.num_rows} rows into {self.dataset_id}:{self.table_id}.")
            print(f"Loaded {table.num_rows} rows into {self.dataset_id}:{self.table_id}.")
        except Exception as e:
            self.logger.error(f"Error uploading to BigQuery: {e}")
            raise


    def execute(self):
        """
        Here, csv_to_dataframe and transmit_to_bigquery are executed.
        """
        self.log_newline()
        self.logger.info("Execution now in process...")

        try:
            self.validate_dataset_existence()
            self.csv_to_dataframe()
            self.transmit_to_bigquery()
            self.logger.info("Execution completed successfully!")
        except Exception as e:
            self.logger.error(f"Execution failed: {e}")
            raise
