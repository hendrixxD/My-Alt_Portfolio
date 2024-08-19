# from airflow import DAG
# from datetime import datetime
# from airflow.utils.dates import days_ago
# from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
# from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# tables = [
#     'olist_customers',
#     'olist_geolocation',
#     'olist_order_items',
#     'olist_order_payments',
#     'olist_order_reviews',
#     'olist_orders',
#     'olist_products',
#     'olist_sellers',
#     'product_category_name_translation'
# ]

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': days_ago(1),
#     'email_on_failure': True,
#     'email_on_retry': True,
#     'retries': 1
# }

# dag = DAG(
#     'postgres_to_bigquery_via_gcs',
#     default_args=default_args,
#     description='An ETL DAG for uploading multiple data from Postgres(source-postgres) to BigQuery(via GCS)',
#     schedule_interval='@once'
# )

# for table in tables:
#     load_data_to_gcs = PostgresToGCSOperator(
#         task_id=f'extract_{table}_to_gcs',
#         postgres_conn_id='source_postgres',
#         gcp_conn_id='google_cloud_default',
#         sql=f'SELECT * FROM cpstn.{table}',
#         bucket='temporary-ecommerce-data-storage',
#         filename=f'data/{table}.json',
#         export_format='json',
#         field_delimiter=',',
#         gzip=False,
#         dag=dag,
#     )

#     load_from_gcs_to_bq = GCSToBigQueryOperator(
#         task_id=f'load_{table}_to_bigquery',
#         bucket='temporary-ecommerce-data-storage',
#         source_objects=[f'data/{table}.json'],
#         destination_project_dataset_table=f'capston.ecommerce.{table}',
#         source_format='NEWLINE_DELIMITED_JSON',
#         write_disposition='WRITE_TRUNCATE',
#         gcp_conn_id='google_cloud_default',
#         dag=dag,
#     )

#     load_data_to_gcs >> load_from_gcs_to_bq

# # VERSION 2
# import yaml
# from airflow import DAG
# from airflow.models import Variable
# from airflow.utils.dates import days_ago
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
# from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
# from airflow.operators.dummy_operator import DummyOperator


# # Load configuration
# with open('./config/config.yml', 'r') as file:
#     config = yaml.safe_load(file)

# #config = Variable.get("etl_config", deserialize_json=True))
# TABLES = config['tables']
# GCP_PROJECT_ID = config['google_cloud']['google_cloud_default']['project_id']
# GCS_BUCKET = config['google_cloud']['google_cloud_default']['gcs_bucket']
# GCS_LOCATION = config['google_cloud']['google_cloud_default']['gcs_location']
# BUCKET_LOCATION = GCP_PROJECT_ID = config['google_cloud']['google_cloud_default']['bucker_location']
# BQ_DATASET = config['google_cloud']['google_cloud_default']['bq_dataset']


# # airflow variables
# postgres_conn__id='source_postgres_db',
# gcp_conn__id='google_cloud_default',

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': days_ago(1),
#     'email_on_failure': True,
#     'email_on_retry': True,
#     'retries': 5
# }

# dag = DAG(
#     'postgres_to_bigquery_etl',
#     default_args=default_args,
#     description='ETL DAG for uploading multiple tables from Postgres to BigQuery via GCS',
#     schedule_interval='@daily',
#     catchup=False
# )

# start = DummyOperator(task_id='start', dag=dag)
# end = DummyOperator(task_id='end', dag=dag)

# def create_table_tasks(table):
#     to_gcs_task = PostgresToGCSOperator(
#         task_id=f'load_{table}_to_gcs',
#         postgres_conn_id=postgres_conn__id,
#         gcp_conn_id=gcp_conn__id,
#         sql=f'SELECT * FROM cpstn.{table}',
#         bucket=GCS_BUCKET,
#         filename=f'data/{table}/{{{{ ds }}}}/{table}.json',
#         export_format='json',
#         gzip=False,
#         dag=dag,
#     )

#     to_bq_task = GCSToBigQueryOperator(
#         task_id=f'load_{table}_to_bigquery',
#         bucket=GCS_BUCKET,
#         source_objects=[f'gs://data/{table}/{{{{ ds }}}}/{table}.json'],
#         destination_project_dataset_table=f'{GCP_PROJECT_ID}.{BQ_DATASET}.{table}',
#         source_format='NEWLINE_DELIMITED_JSON',
#         # schema_object = [f'gs://schemas.json'], # Parameter must be defined if 'schema_fields' is null and autodetect is False.
#         # schema_fields=False,
#         create_disposition="CREATE_IF_NEEDED",
#         write_disposition='WRITE_TRUNCATE',
#         max_bad_records=5,
#         autodetect=True, # Parameter must be set to True if 'schema_fields' and 'schema_object' are undefined.
#         location='europe-west2'
#         gcp_conn_id=gcp_conn__id,
#         dag=dag,
#     )

#     start >> to_gcs_task >> to_bq_task >> end

# for table in TABLES:
#     create_table_tasks(table)

# # VERSION 3
# import yaml
# import logging
# from datetime import timedelta
# from airflow import DAG
# from airflow.models import Variable
# from airflow.utils.dates import days_ago
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
# from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
# from airflow.operators.dummy_operator import DummyOperator
# from airflow.operators.python_operator import PythonOperator
# from airflow.utils.task_group import TaskGroup
# from google.cloud import storage
# from google.cloud import bigquery
# from google.api_core.exceptions import NotFound

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def load_config():
#     """
#     Load configuration from YAML file.
#     """
#     try:
#         with open('./config/config.yml', 'r') as file:
#             return yaml.safe_load(file)
#     except Exception as e:
#         logger.error(f"Failed to load configuration: {str(e)}")
#         raise

# config = load_config()

# TABLES = config['tables']
# GCP_PROJECT_ID = config['google_cloud']['google_cloud_default']['project_id']
# GCS_BUCKET = config['google_cloud']['google_cloud_default']['gcs_bucket']
# GCS_LOCATION = config['google_cloud']['google_cloud_default']['gcs_location']
# BQ_DATASET = config['google_cloud']['google_cloud_default']['bq_dataset']

# # Ensure GCS and BigQuery locations are the same
# BQ_LOCATION = GCS_LOCATION

# # Airflow connection IDs
# POSTGRES_CONN_ID = 'source_postgres_db'
# GCP_CONN_ID = 'google_cloud_default'

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': days_ago(1),
#     'email_on_failure': True,
#     'email_on_retry': True,
#     'retries': 3,
#     'retry_delay': timedelta(minutes=5),
# }

# def check_and_create_gcs_bucket(**kwargs):
#     """
#     Check if the GCS bucket exists. If it does, delete and recreate it.
#     """
#     client = storage.Client(project=GCP_PROJECT_ID)
#     try:
#         bucket = client.get_bucket(GCS_BUCKET)
#         logger.info(f"Bucket {GCS_BUCKET} exists. Deleting and recreating.")
#         bucket.delete(force=True)
#     except NotFound:
#         logger.info(f"Bucket {GCS_BUCKET} does not exist.")
    
#     bucket = client.create_bucket(GCS_BUCKET, location=GCS_LOCATION)
#     logger.info(f"Bucket {GCS_BUCKET} created in {GCS_LOCATION}.")

# def check_and_create_bq_dataset(**kwargs):
#     """
#     Check if the BigQuery dataset exists. If it does, delete and recreate it.
#     """
#     client = bigquery.Client(project=GCP_PROJECT_ID)
#     dataset_id = f"{GCP_PROJECT_ID}.{BQ_DATASET}"
    
#     try:
#         dataset = client.get_dataset(dataset_id)
#         logger.info(f"Dataset {dataset_id} exists. Deleting and recreating.")
#         client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
#     except NotFound:
#         logger.info(f"Dataset {dataset_id} does not exist.")
    
#     dataset = bigquery.Dataset(dataset_id)
#     dataset.location = BQ_LOCATION
#     dataset = client.create_dataset(dataset)
#     logger.info(f"Dataset {dataset_id} created in {BQ_LOCATION}.")

# with DAG(
#     'postgres_to_bigquery_etl',
#     default_args=default_args,
#     description='ETL DAG for uploading multiple tables from Postgres to BigQuery via GCS',
#     schedule_interval='@once',
#     catchup=False,
#     max_active_runs=1
# ) as dag:

#     start = DummyOperator(task_id='start')
    
#     create_gcs_bucket = PythonOperator(
#         task_id='create_gcs_bucket',
#         python_callable=check_and_create_gcs_bucket,
#         provide_context=True,
#     )
    
#     create_bq_dataset = PythonOperator(
#         task_id='create_bq_dataset',
#         python_callable=check_and_create_bq_dataset,
#         provide_context=True,
#     )
    
#     end = DummyOperator(task_id='end')

#     def create_table_tasks(table):
#         with TaskGroup(group_id=f'process_{table}') as tg:
#             to_gcs_task = PostgresToGCSOperator(
#                 task_id=f'load_{table}_to_gcs',
#                 postgres_conn_id=POSTGRES_CONN_ID,
#                 gcp_conn_id=GCP_CONN_ID,
#                 sql=f'SELECT * FROM cpstn.{table}',
#                 bucket=GCS_BUCKET,
#                 filename=f'data/{table}/{{{{ ds }}}}/{table}.json',
#                 export_format='json',
#                 gzip=False,
#             )

#             to_bq_task = GCSToBigQueryOperator(
#                 task_id=f'load_{table}_to_bigquery',
#                 bucket=GCS_BUCKET,
#                 source_objects=[f'data/{table}/{{{{ ds }}}}/{table}.json'],
#                 destination_project_dataset_table=f'{GCP_PROJECT_ID}.{BQ_DATASET}.{table}',
#                 source_format='NEWLINE_DELIMITED_JSON',
#                 create_disposition="CREATE_IF_NEEDED",
#                 write_disposition='WRITE_TRUNCATE',
#                 max_bad_records=5,
#                 autodetect=True,
#                 location=BQ_LOCATION,
#                 gcp_conn_id=GCP_CONN_ID,
#             )

#             to_gcs_task >> to_bq_task

#         return tg

#     table_tasks = [create_table_tasks(table) for table in TABLES]

#     start >> create_gcs_bucket >> create_bq_dataset >> table_tasks >> end

# # Add error handling for the entire DAG
# def handle_error(context):
#     """
#     Handle errors in the DAG execution.
#     """
#     logger.error('An error occurred in the DAG execution:')
#     logger.error(context['exception'])

# dag.on_failure_callback = handle_error

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



# Set up logging
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

    # creates a bigquery dataset if it dosent alrady exist
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
                # filename=f'data/{table}/{{{{ ds }}}}/{table}.json',
                filename=f'data/{table}_{{{{ execution_date.strftime("%Y%m%d_%H%M%S") }}}}.json',
                export_format='json',
                gzip=False,
            )

            to_bq_task = GCSToBigQueryOperator(
                task_id=f'load_{table}_to_bigquery',
                bucket=GCS_BUCKET,
                # source_objects=[f'data/{table}/{{{{ ds }}}}/{table}.json'],
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

# Add error handling for the entire DAG
def handle_error(context):
    """
    Handle errors in the DAG execution.
    """
    logger.error('An error occurred in the DAG execution:')
    logger.error(context['exception'])

dag.on_failure_callback = handle_error
