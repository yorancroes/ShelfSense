import tkinter as tk
from tkinter import messagebox
import psycopg2

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="db",  # Service name from docker-compose.yml
            database="collectors_db",
            user="dummy",
            password="123456"
        )
        messagebox.showinfo("Success", "Connected to the database!")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect: {e}")

root = tk.Tk()
root.title("GUI App")
connect_button = tk.Button(root, text="Connect to Database", command=connect_to_db)
connect_button.pack(pady=20)
root.mainloop()
