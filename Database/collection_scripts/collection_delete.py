from Database.database_scripts.connect import connect_db

def delete_collection(collection_id):
    """
    :param collection_id: The ID of the collection to be deleted from the database.
    :return: None
    """
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM collections WHERE id = %s;", (collection_id,))
        connection.commit()
        print(f"Collection {collection_id} deleted successfully.")

    except Exception as e:
        print(f"Error deleting collection {collection_id}: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()
