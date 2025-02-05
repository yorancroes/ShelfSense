from app.Database.database_scripts.connect import connect_db


def init_db():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS vinyls (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE,
            album VARCHAR(255) NOT NULL,
            artist VARCHAR(255),
            image_path VARCHAR(255),
            description VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            publisher VARCHAR(255) NOT NULL,
            image_path VARCHAR(255),
            price FLOAT NOT NULL,
            platform VARCHAR(100),
            release_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            price FLOAT NOT NULL,
            description VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            author VARCHAR(255),
            publisher VARCHAR(255) NOT NULL,
            publication_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]

    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        for query in queries:
            cursor.execute(query)

        conn.commit()
        print("All tables initialized successfully.")

    except Exception as e:
        print("Error initializing the database:", e)

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


