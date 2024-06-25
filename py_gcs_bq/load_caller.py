
from src.csv_to_bq import BigQueryTransmiter
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_env_variable(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable {var_name} not set.")
    return value

if __name__ == "__main__":
    transmitter = BigQueryTransmiter(
        project_id=get_env_variable('PROJECT_ID'),
        dataset_id=get_env_variable('DATASET_ID'),
        table_id=get_env_variable('TABLE_ID'),
        csv_filepath=get_env_variable('CSV_FILEPATH')
    )
    transmitter.execute()
