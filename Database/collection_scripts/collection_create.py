from Database.database_scripts.connect import connect_db


def make_collection(name, description):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO collections (name, description) VALUES (%s, %s) RETURNING id;",
            (name, description)
        )
        collection_id = cursor.fetchone()[0]
        connection.commit()
        print(f"collection created with id: {collection_id}")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

make_collection("test", "test")