from Database.database_scripts.connect import connect_db


def view_collections():
    conn = connect_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM collections')
        collections = cursor.fetchall()

        if collections:
            print("Your Collections:")
            for collection in collections:
                print(f"ID: {collection[0]}")
                print(f"Name: {collection[1]}")
                print(f"Description: {collection[2]}")
                print(f"Created At: {collection[3]}")
                print(f"Item Count: {collection[4]}")
                print("-" * 30)
        else:
            print("No Collections found.")

    except Exception as e:
        print(f"Error retrieving collections: {e}")

    finally:
        cursor.close()
        conn.close()

view_collections()