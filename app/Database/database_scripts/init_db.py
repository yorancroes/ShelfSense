from Database.database_scripts.connect import connect_db


def init_db():
    query1 = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(query1)
        conn.commit()

        print("Database Initialized Successfully.")

    except Exception as e:
        print("Error Initializing the database:", e)

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()
