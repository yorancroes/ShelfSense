from Database.database_scripts.connect import connect_db

def update_collection(collection_id, new_name, new_discription):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE collections SET name = %s, description = %s WHERE id = %s;",
            (new_name, new_discription, collection_id)
        )

        connection.commit()
        print(f"Collection {collection_id} updated successfully.")

    except Exception as e:
        print(f"Error updating collection {collection_id}: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

update_collection(
    1,
    "test2",
    "test2"
)