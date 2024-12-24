import psycopg2
from Database.database_scripts.connect import connect_db

def init_db():
    query1 = """
    CREATE TABLE IF NOT EXISTS Master_User (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(100),
        password VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN NOT NULL DEFAULT FALSE
    );
    """

    conn = None
    cursor = None

    try:
        # Connect to the database
        conn = connect_db()
        cursor = conn.cursor()

        # Execute the table creation query
        cursor.execute(query1)
        conn.commit()

        print("Database Initialized Successfully.")

    except Exception as e:
        print("Error Initializing the database:", e)

    finally:
        # Close the cursor and connection if they exist
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
