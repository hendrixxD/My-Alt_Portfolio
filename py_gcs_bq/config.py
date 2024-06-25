from src.extract_and_load import APIExtractAndLoad
from src.csv_to_bq import BigQueryTransmiter
from src.get_env_var import get_env_variable
import os


if __name__ == "__main__":
    """
    The First part of the task: uploadind flat csv file to bigquery
    """
    transmitter = BigQueryTransmiter(
        project_id=get_env_variable('PROJECT_ID'),
        dataset_id=get_env_variable('DATASET_ID'),
        table_id=get_env_variable('TABLE_ID'),
        csv_filepath=get_env_variable('CSV_FILEPATH')
    )
    print()
    transmitter.execute()


if __name__ == "__main__":
    """
    The second part of the task:
        - fetch data from an api
        - load to gcs, and
        - write to bigquery
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    extractload = APIExtractAndLoad(
        project_id=get_env_variable('PROJECT_ID'),
        dataset_id=get_env_variable('GCS_DATASET_ID'),
        table_id=get_env_variable('GCS_TABLE_ID'),
        api_uri=get_env_variable('API_URI'),
        file_name=get_env_variable('FILE_NAME'),
        bucket_name=get_env_variable('BUCKET_NAME'),
        path=os.path.join(script_dir, get_env_variable('JSON_PATH'))
    )
    print()
    extractload.execute()
    print()
