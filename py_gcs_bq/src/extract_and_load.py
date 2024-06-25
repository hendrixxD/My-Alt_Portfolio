from .fetch_api_data import fetch_and_save_data
from google.cloud import bigquery
from google.cloud import storage
from io import StringIO
import requests
import logging
import json
import os

class APIExtractAndLoad:
    """
    Initializing credentials
    """
    def __init__(self, project_id, dataset_id, table_id, file_name, api_uri, bucket_name, path):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.file_name = file_name
        self.api_uri = api_uri
        self.bucket_name = bucket_name
        self.path = path
        self.bq_client = bigquery.Client()
        self.gcs_client = storage.Client()

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('apiextractandload.log'),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(__name__)


    def validate_bucket_existence(self):
        """
        Validates the existence of a GCS bucket, else creates a new one.
        """
        try:
            self.gcs_client.get_bucket(self.bucket_name)
            self.logger.info(f"GCS Bucket `{self.bucket_name}` already exists.")

        except Exception as err:
            self.logger.info(f"GCS Bucket `{self.bucket_name}` does not exist, Creating One...")

            bucket = self.gcs_client.bucket(self.bucket_name)
            bucket.storage_class = "STANDARD"

            self.gcs_client.create_bucket(bucket, location="europe-west1")
            self.logger.info(f"Created bucket `{bucket.name}` in `{bucket.location}` with storage class {bucket.storage_class}")


    # def fetch_data_from_api(self):
    #     """
    #     Extracts data from the given API:
    #         `https://sampleapis.com/api-list/playstation/games` and saves to a file
    #     """

    #     self.logger.info(f"Fetching data from `{self.api_uri}`...")

    #     try:
    #             # an independent fuction that pulls json data and saves locally
    #             fetch_and_save_data()
    #             # self.logger.info(f"Successfully Fetched and Saved Json Data to `{self.path}`!")

    #     except Exception as err:
    #         self.logger.error(f"Error fetching data from {self.api_uri}: {err}, Ooops!!")
    #         return        


    def write_api_data_to_gcs(self):
        """
        writes data fetched from an api to gcs storage
        """
        self.logger.info(f"Uploading playstation-data from {self.path} to gcs bucket: {self.bucket_name}...")

        try:
            with open(self.path, 'r', encoding="utf-8") as f:
                saved_json_data = f.read()

            data = json.loads(saved_json_data)

            # to be able to load to gcs, saved_json_data have to be converted to jsonlines
            jsonlines_data = "\n".join(json.dumps(record) for record in data)

            blob = self.gcs_client.bucket(self.bucket_name).blob(self.file_name)

            blob.upload_from_string(jsonlines_data, content_type="application/json")

            self.logger.info(f"Data successfully Uploaded to `gs://{self.bucket_name}/{self.file_name}` in gcs bucket: `{self.bucket_name}`")
        
        except Exception as err:
            self.logger.error(f"Error uploadind data: {err}")
            raise


    def validate_dataset_existence(self):
        """
        Check if the dataset exists in BigQuery, else, it creates it.
        """
        dataset_ref = bigquery.DatasetReference(self.project_id, self.dataset_id)

        try:
            self.bq_client.get_dataset(dataset_ref)
            self.logger.info(f"Dataset `{self.dataset_id}` already exists.")

        except Exception:
            # Creates a dataset if it doesn't exist
            self.logger.info(f"Dataset `{self.dataset_id}` does not exist. Creating a dataset.")
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "europe-west1"

            self.bq_client.create_dataset(dataset)
            self.logger.info(f"Dataset `{self.dataset_id}` created.")


    def loads_data_from_gcs_to_bq(self):
        """
        Loads data from GCS to BigQuery.
        """
        self.logger.info(f"Loading data from gcs bucket: `gs://{self.bucket_name}/{self.file_name}` to bigquery table: `{self.dataset_id}.{self.table_id}`...")

        try:
            table_ref = self.bq_client.dataset(self.dataset_id).table(self.table_id)

            schema = [
                bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("genre", "STRING", mode="REPEATED"),
                bigquery.SchemaField("developers", "STRING", mode="REPEATED"),
                bigquery.SchemaField("publishers", "STRING", mode="REPEATED"),
                bigquery.SchemaField(
                    "ReleaseDates", "RECORD", mode="NULLABLE",
                    fields = [
                        bigquery.SchemaField("Japan", "STRING", mode="NULLABLE"),
                        bigquery.SchemaField("NorthAmerica", "STRING", mode="NULLABLE"),
                        bigquery.SchemaField("Europe", "STRING", mode="NULLABLE"),
                        bigquery.SchemaField("Australia", "STRING", mode="NULLABLE"),
                    ]
                )
            ]

            job_config = bigquery.LoadJobConfig(
                schema=schema,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
            )

            load_job = self.bq_client.load_table_from_uri(
                f"gs://{self.bucket_name}/{self.file_name}",
                table_ref,
                job_config=job_config,
                # this is the same location as the dataset location
                location="europe-west1"
            )

            load_job.result()

            self.logger.info(f"Loaded {load_job.output_rows} rows into {self.dataset_id}:{self.table_id}.")

        except Exception as err:
            self.logger.error(f"Error loading data to BigQuery: {err}")
            raise


    def execute(self):
        """
        Executes the E&L process
            - validate GCS bucket
            - fetch data
            - write api data to gcs
            - validate bq dataset existence
            - load data to bg from gcs
        """
        self.logger.info("Starting E&L process...")

        try:
            # 1
            self.validate_bucket_existence()
            
            # 2 - Fetches json data
            try:
                 response = requests.get('https://api.sampleapis.com/playstation/games')
                 response.raise_for_status()
                 data = response.json()
            except requests.exceptions.RequestException as err:
                 return f"Error fetching data: {err}"
            
            try:
                with open('./data/playstation.json', 'w', encoding='utf-8') as outfile:
                    StringIO(json.dump(data, outfile, indent=4))
                print(f"Data saved successfully to: './data/playstation.json'")
            except OSError as err:
                print(f"Error saving data: {err}")

            # 3
            self.write_api_data_to_gcs()

            # 4
            self.validate_dataset_existence()

            # 5
            self.loads_data_from_gcs_to_bq()
            self.logger.info("E&L process completed successfully.")

        except Exception as err:
            self.logger.error(f"E&L process failed: {err}")
            raise
