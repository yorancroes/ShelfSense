import os
import tkinter as tk
from tkinter import messagebox
import psycopg2

def connect_to_db():
    try:
        # Get database connection details from environment variables
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", 5432)
        db_name = os.getenv("DB_NAME", "collectors_db")
        db_user = os.getenv("DB_USER", "dummy")
        db_password = os.getenv("DB_PASSWORD", "123456")

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        messagebox.showinfo("Success", "Connected to the database!")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect: {e}")

# Set up the Tkinter window
root = tk.Tk()
root.title("Database Connection Test")

# Create a button to trigger the connection attempt
connect_button = tk.Button(root, text="Connect to Database", command=connect_to_db)
connect_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
