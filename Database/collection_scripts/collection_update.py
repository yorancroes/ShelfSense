from Database.database_scripts.connect import connect_db

def update_collection(collection_id, new_name, new_discription):
    """
    :param collection_id: The unique identifier of the collection to be updated
    :param new_name: The new name to assign to the collection
    :param new_discription: The new description to assign to the collection
    :return: None
    """
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


def update_collection_name(collection_id, new_name):
    """
    :param collection_id: The ID of the collection to be updated.
    :param new_name: The new name to assign to the collection.
    :return: None
    """
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE collections SET name = %s WHERE id = %s;",
            (new_name, collection_id)
        )
        connection.commit()
        print(f"Collection {collection_id} updated successfully.")

    except Exception as e:
        print(f"Error updating collection {collection_id}: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def update_collection_description(collection_id, new_description):
    """
    :param collection_id: The unique identifier of the collection to update.
    :param new_description: The new description to set for the specified collection.
    :return: None
    """
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE collections SET description = %s WHERE id = %s;",
            (new_description, collection_id)
        )
        connection.commit()
        print(f"Collection {collection_id} updated successfully.")

    except Exception as e:
        print(f"Error updating collection {collection_id}: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()