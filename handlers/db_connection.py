import psycopg2
from tkinter import ttk, messagebox


def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='sosadatabase',
            user='postgres',
            password='mQHiLhyE5@h728CEcD',
            host='localhost',
            port='5432'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None
