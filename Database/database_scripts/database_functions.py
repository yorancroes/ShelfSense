from Database.database_scripts.connect import connect_db

# Function to add a column to a table
#TODO: revise later that it can handle multiple columns at once.

def add_column(table_name, column_name, column_type):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        allowed_types =  ["TEXT", "INTEGER", "REAL", "BOOLEAN", "DATE", "TIMESTAMP"]
        if column_type.upper() not in allowed_types:
            raise ValueError(f"Invalid column type: {column_type}")

        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")
        connection.commit()
        print(f"Column {column_name} added to table {table_name} successfully.")

    except Exception as e:
        print(f"Error adding column {column_name} to table {table_name}: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

# FUnction to get the collection_id of given collection
def get_collection_id(collection_name):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM collections WHERE name = %s;", (collection_name,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            # Handle the case where no results were found
            return None
    except Exception as e:
        # Handle the exception (e.g., log the error)
        print(f"An error occurred: {e}")
        return None
