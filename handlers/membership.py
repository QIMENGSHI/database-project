import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import random
from handlers.db_connection import connect_db
from gui.windows import create_board_member_window


def verify_membership(member_id_entry):
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        membership_id = membership_id_entry.get()
        try:
            cur.execute(
                "SELECT * FROM Membership WHERE MembershipID = %s", (membership_id,))
            member = cur.fetchone()
            if member:
                messagebox.showinfo("Login Successful", "Welcome back!")

            else:
                messagebox.showwarning(
                    "Membership Not Found", "Membership ID not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()
            conn.close()
    else:
        messagebox.showwarning("Connection Failed",
                               "Failed to connect to the database.")


def generate_membership_id():
    # Generate a unique 6-digit number as MembershipID
    return random.randint(100000, 999999)
