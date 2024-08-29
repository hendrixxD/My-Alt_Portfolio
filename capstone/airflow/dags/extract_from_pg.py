#
# -----------------------------------------------------------------------------------------------
# VERSION 4
# -----------------------------------------------------------------------------------------------
#  
import yaml
import logging
from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator



# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    """
    Load configuration from YAML file.
    """
    try:
        with open('./config/config.yml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        raise

config = load_config()

TABLES = config['tables']
GCP_PROJECT_ID = config['google_cloud']['google_cloud_default']['project_id']
GCS_BUCKET = config['google_cloud']['google_cloud_default']['gcs_bucket']
BQ_DATASET = config['google_cloud']['google_cloud_default']['bq_dataset']
GCS_LOCATION = config['google_cloud']['google_cloud_default']['gcs_location']

# Ensure GCS and BigQuery locations are the same
BQ_LOCATION = GCS_LOCATION

# Airflow connection IDs
POSTGRES_CONN_ID = 'source_postgres_db'
GCP_CONN_ID = 'google_cloud_default'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'postgres_to_bigquery_etl',
    default_args=default_args,
    description='ETL DAG for uploading multiple tables from Postgres to BigQuery via GCS',
    schedule_interval='@once',
    catchup=False,
    max_active_runs=1
) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    # Create GCS bucket if it doesn't exist
    create_bucket = GCSCreateBucketOperator(
        task_id='create_gcs_bucket',
        bucket_name=GCS_BUCKET,
        project_id=GCP_PROJECT_ID,
        location=GCS_LOCATION,
        storage_class='REGIONAL',
        gcp_conn_id=GCP_CONN_ID
    )

    # create a bigquery dataset if it dosent alrady exist
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_bigquery_dataset',
        dataset_id=BQ_DATASET,
        project_id=GCP_PROJECT_ID,
        location=BQ_LOCATION,
        exists_ok=True,
        gcp_conn_id=GCP_CONN_ID
    )

    def create_table_tasks(table):
        with TaskGroup(group_id=f'process_{table}') as tg:
            to_gcs_task = PostgresToGCSOperator(
                task_id=f'load_{table}_to_gcs',
                postgres_conn_id=POSTGRES_CONN_ID,
                gcp_conn_id=GCP_CONN_ID,
                sql=f'SELECT * FROM cpstn.{table}',
                bucket=GCS_BUCKET,
                filename=f'data/{table}_{{{{ execution_date.strftime("%Y%m%d_%H%M%S") }}}}.json',
                export_format='json',
                gzip=False,
            )

            to_bq_task = GCSToBigQueryOperator(
                task_id=f'load_{table}_to_bigquery',
                bucket=GCS_BUCKET,
                source_objects=[f'data/{table}_{{{{ execution_date.strftime("%Y%m%d_%H%M%S") }}}}.json'],
                destination_project_dataset_table=f'{GCP_PROJECT_ID}.{BQ_DATASET}.{table}',
                source_format='NEWLINE_DELIMITED_JSON',
                create_disposition="CREATE_IF_NEEDED",
                write_disposition='WRITE_TRUNCATE',
                max_bad_records=5,
                autodetect=True,
                gcp_conn_id=GCP_CONN_ID,
            )

            to_gcs_task >> to_bq_task

        return tg

    table_tasks = [create_table_tasks(table) for table in TABLES]

    start >> create_bucket >> create_dataset >> table_tasks >> end

# error handling for the entire DAG
def handle_error(context):
    """
    Handle errors in the DAG execution.
    """
    logger.error('An error occurred in the DAG execution:')
    logger.error(context['exception'])

dag.on_failure_callback = handle_error
