from Database.database_scripts.connect import connect_db

def create_item_table(collection_id, collection_name):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        table_name = f"items__{collection_name}_{collection_id}"
        cursor.execute(
            f"""
            CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY,
                
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT,
                FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE
            );
            """
        )
        cursor.execute(
            "UPDATE collections SET item_table_id = %s WHERE id = %s;",
            (table_name, collection_id)
        )
        connection.commit()
        updated_id = cursor.fetchone()[0]

        print(f"Table '{table_name}' created successfully.")
        return updated_id

    except Exception as e:
        print(f"Error creating table: {e}")
        connection.rollback()
        return None

    finally:
        cursor.close()
        connection.close()


