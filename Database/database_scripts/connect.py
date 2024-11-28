import psycopg2

def connect_db():
    try:
        connection = psycopg2.connect(
            dbname="collectors_db",
            user="dummy",
            password="123456",
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