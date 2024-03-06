import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import random


def add_event(root):
    # Function to open a new window for adding an event
    add_event_window = tk.Toplevel(root)
    add_event_window.title("Add New Event")

    # Event Name Entry
    tk.Label(add_event_window, text="Event Name:").grid(
        row=0, column=0, padx=10, pady=10)
    event_name_entry = tk.Entry(add_event_window)
    event_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Event Date Entry
    tk.Label(add_event_window, text="Event Date (YYYY-MM-DD):").grid(row=1,
                                                                     column=0, padx=10, pady=10)
    event_date_entry = tk.Entry(add_event_window)
    event_date_entry.grid(row=1, column=1, padx=10, pady=10)

    # Submit Button
    submit_btn = tk.Button(add_event_window, text="Submit", command=lambda: submit_new_event(
        event_name_entry, event_date_entry, add_event_window, root))
    submit_btn.grid(row=2, column=0, columnspan=2, pady=10)
    pass


def submit_new_event(event_name_entry, event_date_entry, add_event_window, root):
    # Function to insert the new event into the database
    event_name = event_name_entry.get()
    event_date = event_date_entry.get()

    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO Event (EventName, EventDate) VALUES (%s, %s)", (event_name, event_date))
            conn.commit()
            messagebox.showinfo(
                "Success", "Event added successfully.", parent=add_event_window)
            add_event_window.destroy()  # Close the add event window
            # Optionally refresh the event management interface
            event_management(root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=add_event_window)
        finally:
            cur.close()
            conn.close()
