from Database.database_scripts.connect import connect_db

# creates a collection
def create_collection(name, description):
    """
    :param name: The name of the collection to be created in the database.
    :param description: A brief description of the collection.
    :return: The name of the collection that was successfully created.
    """
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

    return name


# def add_collection_image(collection_id, image_file_path):
#     connection = connect_db()
#     cursor = connection.cursor()
#
#     try:
#         with open(image_file_path, "rb") as image_file:
#             image_data = image_file.read()
#
#         cursor.execute(
#             "Update collections SET image_data = %s WHERE id = %s;",
#             (image_data, collection_id)
#         )
#         connection.commit()
#         print(f"Collection image added successfully.")
#
#     except Exception as e:
#         print(f"Error adding collection image: {e}")
#         connection.rollback()
#
#     finally:
#         cursor.close()
#         connection.close()

