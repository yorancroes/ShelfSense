import bcrypt
from Database.database_scripts.connect import connect_db



class User:
    def __init__(self, username, password):
        self.username = username
        self.hashed_password = self.hash_password(password)

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def verify_password(self):
        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT password FROM users WHERE username = %s", (self.username,))
            stored_hashed_password = cursor.fetchone()

            if stored_hashed_password == self.hashed_password:
                return True
            else:
                return False

        except Exception as e:
            print("Error verifying password: ", e)

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
            print("error inserting user into the database", e)

        finally:
            if cursor is not None:
                cursor.close()

            if conn is not None:
                conn.close()

    def test_user(self):
        print("username:", self.username, "password:", self.hashed_password)
