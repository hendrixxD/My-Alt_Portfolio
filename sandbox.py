from google.cloud import biwquery
from dotenv import load_dotenv

import logging

logging.basicConfig(level=logging.INFO, format=":%(asctime)s:%(levelname)s:%(message)s")

load_dotenv()


PROJECT_ID = 'my-altschool-dev'
DATASET_ID = 'etl_intro'
TABLE_ID = 'fake_bank'
logging.info('Testing the logger')

client = bigquery.Client(PROJECT_ID=PROJECT_ID)

# dataset creation
dataset_ref = client.dataset(DATASET_ID)
dataset = client.create_dataset(dataset_ref)


logging.info(f"Dataset {DATASET_ID} created")

table_ref = 'mbank_transaction'

 
# table creation
	# opt1- use a ddl statemnt from python
	# opt2- use a bq schema
	# op1-3 use a json file holdin table schema from python
	# infer table schema

# ddl = """
# create table my-altschool-dev.etl_intro.bank_transaction (
# 	id int64,
# 	category string,
# 	description string,
# 	debit float64,
# 	credit float64,
# 	transctionDate string,
# )
# """

schema = [

]

query_job = client.query(ddl)

query_job.result


# DDL and DML Manipulation
 