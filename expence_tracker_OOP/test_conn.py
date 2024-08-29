import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
    host=os.environ.get('host'),
    port=os.environ.get('port'),
    dbname=os.environ.get('dbname'),
    user=os.environ.get('user'),
    password=os.environ.get('password')
)

with connection as conn:
    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS exams.testing (
                id serial,
                title Varchar(255),
                amount float,
                created_at timestamp,
                updated_at timestamp
                )
            """
            )
        print()
        print("Connection successful!!")

host=os.environ.get('host')
port=os.environ.get('port')
dbname=os.environ.get('dbname')
user=os.environ.get('user')
password=os.environ.get('password')

print("Host:", host, "Port:", port, "DBname:", dbname, "User:", user, "Password:", password)
print()
