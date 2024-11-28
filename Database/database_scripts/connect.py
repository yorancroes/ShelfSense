import psycopg2
from config import config
from config import *
# use this to setup a connection to the database.
def connect_db():
    try:
        connection = psycopg2.connect(
            dbname="collectors_db",
            user=config.username,
            password=config.password,
            host="localhost",
            port="5432"
        )
        print("Database connection successful!")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

db = connect_db()
if db:
    db.close()