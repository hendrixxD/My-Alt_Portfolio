import os
import psycopg2
from dotenv import load_dotenv

# load environment variables
load_dotenv()

connection = psycopg2.connect(
    host=os.environ.get('host'),
    port=os.environ.get('port'),
    dbname=os.environ.get('dbname'),
    user=os.environ.get('user'),
    password=os.environ.get('password')
)

# creates a cursor for execution of sql queries
cur = connection.cursor()


def count_record():
	cur.execute(
		"SELECT COUNT(*) FROM assignement.crypto_prices;"
	)

	result = cur.fetchall()

	print(result)



if __name__=="__main__":
	count_record()