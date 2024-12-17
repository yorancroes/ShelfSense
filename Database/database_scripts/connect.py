import psycopg2
from tkinter import messagebox, Tk

# Function to set up a connection to the database
def connect_db():
    try:
        connection = psycopg2.connect(
            dbname="collectors_db",
            user="dummy",
            password="123456",
            host="db",
            port="5432"
        )
        return connection
    except Exception as e:
        return None
