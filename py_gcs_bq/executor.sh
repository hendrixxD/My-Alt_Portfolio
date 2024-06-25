#!/bin/bash

# before runing this script, set your credentials in the .env correctly
# see .env.example
#
# install dependencies
pip install -r requirements.txt


# if you use `python` to run your python scripts change it below, eg _python exam.py_
# This will execute the first and second part of the task:
# loading CSV data to bigquery, 
# fetching data from an API, loading to gcs and writing to bq

python3 config.py