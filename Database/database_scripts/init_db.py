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


    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(query1)
        conn.commit()

        print("Database Initialized Succesfully.")

    except Exception as e:
        print("Error Initlializing the database", e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()
