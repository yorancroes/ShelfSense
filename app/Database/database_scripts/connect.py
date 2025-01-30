import psycopg2

# Function to set up a connection to the database
def connect_db():
    try:
        connection = psycopg2.connect(
            dbname="collectors_db",
            user="dummy",
            password="123456",
            host="localhost",
            port="5433"
        )
        return connection

    except Exception as e:
        print(f"error {e}")
        return None
