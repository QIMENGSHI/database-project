import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import random
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='sosadatabase',
            user='sosadatabase',
            password='Qn6616',
            host='localhost',
            port='5432'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None
def create_board_member_window():
    window = tk.Toplevel()
    window.title("Board Member Management")

    # Buttons for different management options
    ttk.Button(window, text="Event Management", command=event_management).grid(column=0, row=0, sticky=tk.W, pady=10)
    ttk.Button(window, text="Membership Management", command=membership_management).grid(column=0, row=1, sticky=tk.W, pady=10)
    ttk.Button(window, text="Student Management", command=student_management).grid(column=0, row=2, sticky=tk.W, pady=10)
    ttk.Button(window, text="StudentMembership Management", command=student_membership_management).grid(column=0, row=3, sticky=tk.W, pady=10)
    ttk.Button(window, text="EventRegistration Management", command=event_registration_management).grid(column=0, row=4, sticky=tk.W, pady=10)

    # Example function for one of the management options
    def event_management(root):
    # Clear the current window
        for widget in root.winfo_children():
            widget.destroy()

    # Fetch events from the database
        conn = connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT EventID, EventName, EventDate FROM Event")
            events = cur.fetchall()

    # Display the events in a simple table format
        headers = ['Event ID', 'Event Name', 'Event Date']
        for i, header in enumerate(headers):
            ttk.Label(root, text=header).grid(row=0, column=i)

        for i, event in enumerate(events):
            for j, value in enumerate(event):
                ttk.Label(root, text=value).grid(row=i+1, column=j)

    # Buttons for CRUD operations
        ttk.Button(root, text="Add Event", command=lambda: add_event(root)).grid(columnspan=len(headers), sticky=tk.W, pady=10)
        ttk.Button(root, text="Update Event", command=lambda: update_event_prompt(root)).grid(columnspan=len(headers), sticky=tk.W, pady=10)
        ttk.Button(root, text="Delete Event", command=lambda: delete_event_prompt(root)).grid(columnspan=len(headers), sticky=tk.W, pady=10)

        cur.close()
        conn.close()
    
        
    def add_event(root):
    # Function to open a new window for adding an event
        add_event_window = tk.Toplevel(root)
        add_event_window.title("Add New Event")

    # Event Name Entry
        tk.Label(add_event_window, text="Event Name:").grid(row=0, column=0, padx=10, pady=10)
        event_name_entry = tk.Entry(add_event_window)
        event_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Event Date Entry
        tk.Label(add_event_window, text="Event Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
        event_date_entry = tk.Entry(add_event_window)
        event_date_entry.grid(row=1, column=1, padx=10, pady=10)

    # Submit Button
        submit_btn = tk.Button(add_event_window, text="Submit", command=lambda: submit_new_event(event_name_entry, event_date_entry, add_event_window, root))
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
                cur.execute("INSERT INTO Event (EventName, EventDate) VALUES (%s, %s)", (event_name, event_date))
                conn.commit()
                messagebox.showinfo("Success", "Event added successfully.", parent=add_event_window)
                add_event_window.destroy()  # Close the add event window
                event_management(root)  # Optionally refresh the event management interface
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=add_event_window)
            finally:
                cur.close()
                conn.close()
def verify_membership():
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        membership_id = membership_id_entry.get()
        try:
            cur.execute("SELECT * FROM Membership WHERE MembershipID = %s", (membership_id,))
            member = cur.fetchone()
            if member:
                messagebox.showinfo("Login Successful", "Welcome back!")
                create_board_member_window()
                
            else:
                messagebox.showwarning("Membership Not Found", "Membership ID not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()
            conn.close()
    else:
        messagebox.showwarning("Connection Failed", "Failed to connect to the database.")

# Set up the login window
root = tk.Tk()
root.title("SoSA Member Login")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Membership ID entry 
membership_id_entry = ttk.Entry(mainframe, width=30)
membership_id_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
ttk.Label(mainframe, text="Membership ID").grid(column=1, row=1, sticky=tk.W)

# Login button
ttk.Button(mainframe, text="Login", command=verify_membership).grid(column=2, row=2, sticky=tk.W)

# Registration button
ttk.Button(mainframe, text="Register as Member", command=lambda: registration_window(root)).grid(column=2, row=3, sticky=tk.W)

def generate_membership_id():
    # Generate a unique 6-digit number as MembershipID
    return random.randint(100000, 999999)

def registration_window(parent):
    reg_win = tk.Toplevel(parent)
    reg_win.title("Register as SoSA Member")

    reg_frame = ttk.Frame(reg_win, padding="10 10 10 10")
    reg_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    reg_win.columnconfigure(0, weight=1)
    reg_win.rowconfigure(0, weight=1)

    # Inputs: Student ID, Name, Email, StartDate, ExpireDate, MembershipType
    inputs = ["Student ID", "Name", "Email", "Start Date", "Expire Date", "Membership Type"]
    entries = {}
    for idx, input in enumerate(inputs, start=1):
        ttk.Label(reg_frame, text=input).grid(column=1, row=idx, sticky=tk.W)
        entry_var = tk.StringVar()
        entries[input] = ttk.Entry(reg_frame, width=30, textvariable=entry_var)
        entries[input].grid(column=2, row=idx, sticky=(tk.W, tk.E))
    
    # Submit button for registration
    ttk.Button(reg_frame, text="Submit", command=lambda: submit_registration(entries, reg_win)).grid(column=2, row=len(inputs) + 1, sticky=tk.W)

def submit_registration(entries, window):
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            # Insert into Student table
            student_id = entries["Student ID"].get()
            name = entries["Name"].get()
            email = entries["Email"].get()
            cur.execute("INSERT INTO Student (StudentID, Name, Email) VALUES (%s, %s, %s)", (student_id, name, email))

            # Generate MembershipID and insert into Membership table
            membership_id = generate_membership_id()
            membership_type = entries["Membership Type"].get()
            start_date = entries["Start Date"].get()
            expire_date = entries["Expire Date"].get()
            cur.execute("INSERT INTO Membership (MembershipID, MembershipType, StartDate, ExpireDate) VALUES (%s, %s, %s, %s)",
                        (membership_id, membership_type, start_date, expire_date))

            # Link Student with Membership in StudentMembership table
            cur.execute("INSERT INTO StudentMembership (StudentID, MembershipID) VALUES (%s, %s)", (student_id, membership_id))

            # Commit the transactions
            conn.commit()

            # Inform the user of successful registration and their MembershipID
            messagebox.showinfo("Registration Successful", f"You are now registered. Your Membership ID is {membership_id}.")
            window.destroy()

        except Exception as e:
            messagebox.showerror("Registration Error", str(e))
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    pass

# Run the login application
root.mainloop()

    