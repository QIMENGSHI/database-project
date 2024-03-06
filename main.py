import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import random
from gui.windows import *


# Main window
root = tk.Tk()
root.title("SoSA Memberbership Management")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Membership ID entry 
membership_id_entry = ttk.Entry(mainframe, width=30)
membership_id_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
ttk.Label(mainframe, text="Membership ID").grid(
    column=1, row=1, sticky=tk.W)

# Login button
ttk.Button(mainframe, text="Login", command=verify_membership(membership_id_entry)).grid(
    column=2, row=2, sticky=tk.W)

# Registration button
ttk.Button(mainframe, text="Register as Member", command=lambda: registration_window(
    root)).grid(column=2, row=3, sticky=tk.W)

# Run the login application
root.mainloop()
