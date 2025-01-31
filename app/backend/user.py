import bcrypt
from app.Database.database_scripts.connect import connect_db
#TODO: MAKE GET USER_ID METHOD

class User:
    def __init__(self, username, password):
        self.username = username
        self.hashed_password = self.hash_password(password)

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def get_username(self):
        return self.username

    def verify_password(self, password):
        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT password FROM users WHERE username = %s", (self.username,))
            result = cursor.fetchone()

            if result is None:
                return False

            stored_hashed_password = result[0]

            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                return True
            else:
                return False

        except Exception as e:
            print("Error verifying password: ", e)
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def insert_user(self):
        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                           (self.username, self.hashed_password))
            conn.commit()
            print("User inserted successfully")

        except Exception as e:
            print("Error inserting user into the database: ", e)

        finally:
            if cursor is not None:
                cursor.close()

            if conn is not None:
                conn.close()



    def test_user(self):
        print("username:", self.username, "password:", self.hashed_password)
