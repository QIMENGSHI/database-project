import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import random


def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='sosadatabase',
            user='postgres',  # postgres
            password='mQHiLhyE5@h728CEcD',  # mQHiLhyE5@h728CEcD
            host='localhost',
            port='5432'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None


def submit_delete_registration(membership_id, event_id, window, root):
    conn = connect_db()
    if conn is None:
        messagebox.showwarning("Connection Failed", "Failed to connect to the database.")
        return

    try:
        cur = conn.cursor()
        # Delete the specified registration
        cur.execute("DELETE FROM EventRegistration WHERE MembershipID = %s AND EventID = %s", (membership_id, event_id))
        conn.commit()

        if cur.rowcount == 0:  # No rows deleted
            messagebox.showinfo("Delete Unsuccessful", "No registration found with the provided Membership ID and Event ID.")
        else:
            messagebox.showinfo("Delete Successful", "The registration has been successfully deleted.")
            
        window.destroy()
        event_registration_management(root)
        
    except Exception as e:
        messagebox.showerror("Deletion Error", str(e))
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def delete_registration_prompt(event_id, parent_window, root):
    delete_window = tk.Toplevel(parent_window)
    delete_window.title("Delete Registration")

    tk.Label(delete_window, text="Membership ID:").grid(row=0, column=0)
    membership_id_entry = tk.Entry(delete_window)
    membership_id_entry.grid(row=0, column=1)

    tk.Label(delete_window, text="Event ID:").grid(row=1, column=0)
    event_id_entry = tk.Entry(delete_window)
    event_id_entry.insert(0, str(event_id))  # Pre-fill with the event ID, make it read-only if you prefer
    event_id_entry.grid(row=1, column=1)

    # Delete button
    delete_btn = tk.Button(delete_window, text="Delete", command=lambda: submit_delete_registration(membership_id_entry.get(), event_id_entry.get(), delete_window, root))
    delete_btn.grid(row=2, column=0, columnspan=2)

def register_for_event(event_id, parent_window):
    # Create the new window for MembershipID input
    reg_input_window = tk.Toplevel(parent_window)
    reg_input_window.title("Event Registration")

    tk.Label(reg_input_window, text="Membership ID:").grid(row=0, column=0)
    membership_id_entry = tk.Entry(reg_input_window)
    membership_id_entry.grid(row=0, column=1)

    # Submit button
    submit_btn = tk.Button(reg_input_window, text="Submit", command=lambda: submit_event_registration(event_id, membership_id_entry.get(), reg_input_window))
    submit_btn.grid(row=1, column=0, columnspan=2)

def submit_event_registration(event_id, membership_id, window,):
    conn = connect_db()
    if conn is None:
        messagebox.showwarning("Connection Failed", "Failed to connect to the database.")
        return

    try:
        cur = conn.cursor()
        # Check if the membership ID exists
        cur.execute("SELECT * FROM Membership WHERE MembershipID = %s", (membership_id,))
        if cur.fetchone() is None:
            messagebox.showerror("Registration Error", "Invalid Membership ID.")
            return
        
        # Insert the registration data into the database
        cur.execute("INSERT INTO EventRegistration (MembershipID, EventID) VALUES (%s, %s)", (membership_id, event_id))
        conn.commit()
        messagebox.showinfo("Registration Successful", "You have successfully registered for the event.")
        window.destroy()
        
    except Exception as e:
        messagebox.showerror("Registration Error", str(e))
        conn.rollback()
    finally:
        cur.close()
        conn.close()

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


def delete_event(event_id, root):
    print("Begin deletion")
    print(event_id)
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            print("Deleting")
            cur.execute("DELETE FROM Event WHERE EventID = %s", (event_id,))
            conn.commit()
            print("Deleted")
            messagebox.showinfo(
                "Success", "Event deleted successfully.", parent=root)
            print("Message shown")
            # Optionally refresh the event management interface
            event_management(root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=root)
        finally:
            cur.close()
            conn.close()


def update_event(event_id, event_name_entry, event_date_entry, update_event_window, root):
    event_name = event_name_entry.get()
    event_date = event_date_entry.get()

    print("Begin update")
    print(event_id)
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE Event SET EventName = %s, EventDate = %s WHERE EventID = %s",
                        (event_name, event_date, event_id))
            conn.commit()
            messagebox.showinfo(
                "Success", "Event updated successfully.", parent=update_event_window)
            event_management(root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=update_event_window)
        finally:
            cur.close()
            conn.close()


def update_event_window(event_id, root):
    print("Begin update window")
    update_event_window = tk.Toplevel(root)
    update_event_window.title("Update Event")

    # Event Name Entry
    tk.Label(update_event_window, text="Event Name:").grid(
        row=0, column=0, padx=10, pady=10)
    event_name_entry = tk.Entry(update_event_window)
    event_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Event Date Entry
    tk.Label(update_event_window, text="Event Date (YYYY-MM-DD):").grid(row=1,
                                                                        column=0, padx=10, pady=10)
    event_date_entry = tk.Entry(update_event_window)
    event_date_entry.grid(row=1, column=1, padx=10, pady=10)

    # Submit Button
    submit_btn = tk.Button(update_event_window, text="Submit", command=lambda: update_event(
        event_id, event_name_entry, event_date_entry, update_event_window, root))
    submit_btn.grid(row=2, column=0, columnspan=2, pady=10)


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
        print(events)
        # print(events[0][0])

    # Display the events in a simple table format
    # Table headers
    headers = ['Event ID', 'Event Name', 'Event Date']
    for i, header in enumerate(headers):
        ttk.Label(root, text=header).grid(row=0, column=i)

    # Table data
    for i, event in enumerate(events):
        for j, value in enumerate(event):
            print(value)
            print(events[i][0])
            ttk.Label(root, text=value).grid(row=i+1, column=j)

            # Delete button for each event, delete according to EventID
            ttk.Button(root, text="Delete", command=lambda event_id=events[i][0]: delete_event(
                event_id, root)).grid(row=i+1, column=len(headers))

            # Update button for each event, update according to EventID
            ttk.Button(root, text="Update", command=lambda event_id=events[i][0]: update_event_window(
                event_id, root)).grid(row=i+1, column=len(headers)+1)

    # Buttons for CRUD operations
    ttk.Button(root, text="Add Event", command=lambda: add_event(
        root)).grid(columnspan=len(headers), sticky=tk.W, pady=10)

    cur.close()
    conn.close()


def delete_member(member_id, root):
    print("Begin deletion")
    print(member_id)
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            # Fetch student ID from StudentMembership
            cur.execute(
                "SELECT StudentID FROM StudentMembership WHERE MembershipID = %s", (member_id,))
            student_id = cur.fetchone()[0]
            print(student_id)

            print("Deleting")
            cur.execute("""BEGIN;
            DELETE FROM EventRegistration 
            WHERE MembershipID = %s;
            
            DELETE FROM StudentMembership
            WHERE MembershipID = %s;
            
            DELETE FROM Student
            WHERE StudentID = %s;
            
            DELETE FROM Membership
            WHERE MembershipID = %s;
            
            COMMIT;""", (member_id, member_id, student_id, member_id))

            conn.commit()
            print("Deleted")
            messagebox.showinfo(
                "Success", "Member deleted successfully.", parent=root)
            print("Message shown")
            # Optionally refresh the event management interface
            membership_management(root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=root)
        finally:
            cur.close()
            conn.close()


def update_member(member_id, member_name_entry, member_email_entry, membership_expiry_date_entry, membership_type_entry, update_member_window, root):
    member_name = member_name_entry.get()
    member_email = member_email_entry.get()
    membership_expiry_date = membership_expiry_date_entry.get()
    membership_type = membership_type_entry.get()

    print("Begin update")
    print(member_id)
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute("""BEGIN;
            UPDATE Membership
            SET MembershipType = %s, ExpireDate = %s
            WHERE MembershipID = %s;
            
            UPDATE Student
            SET Name = %s, Email = %s
            WHERE StudentID = (SELECT StudentID FROM StudentMembership WHERE MembershipID = %s);
            COMMIT;""", (membership_type, membership_expiry_date, member_id, member_name, member_email, member_id))
            conn.commit()
            messagebox.showinfo(
                "Success", "Member updated successfully.", parent=update_member_window)
            membership_management(root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=update_member_window)
        finally:
            cur.close()
            conn.close()


def update_member_window(membership_id, root):
    print("Begin update window")
    update_member_window = tk.Toplevel(root)
    update_member_window.title("Update Membership")

    # Member Name
    tk.Label(update_member_window, text="Member Name:").grid(
        row=0, column=0, padx=10, pady=10)
    member_name_entry = tk.Entry(update_member_window)
    member_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Member Email
    tk.Label(update_member_window, text="Member Email:").grid(row=1,
                                                              column=0, padx=10, pady=10)
    member_email_entry = tk.Entry(update_member_window)
    member_email_entry.grid(row=1, column=1, padx=10, pady=10)

    # Membership expiry date
    tk.Label(update_member_window, text="Membership Expiry Date (YYYY-MM-DD):").grid(row=2,
                                                                                     column=0, padx=10, pady=10)
    membership_expiry_date_entry = tk.Entry(update_member_window)
    membership_expiry_date_entry.grid(row=2, column=1, padx=10, pady=10)

    # Membership type
    tk.Label(update_member_window, text="Membership Type:").grid(row=3,
                                                                 column=0, padx=10, pady=10)
    membership_type_entry = tk.Entry(update_member_window)
    membership_type_entry.grid(row=3, column=1, padx=10, pady=10)

    # Submit Button
    submit_btn = tk.Button(update_member_window, text="Submit", command=lambda: update_member(
        membership_id, member_name_entry, member_email_entry, membership_expiry_date_entry, membership_type_entry, update_member_window, root))
    submit_btn.grid(row=4, column=0, columnspan=2, pady=10)


def membership_management(root):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Fetch events from the database
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("""SELECT Membership.*, Student.*
FROM StudentMembership
INNER JOIN Student ON StudentMembership.StudentID = Student.StudentID
INNER JOIN Membership ON StudentMembership.MembershipID = Membership.MembershipID;""")
        student_members = cur.fetchall()
        print(student_members)

    # Display the events in a simple table format
    # Table headers
    headers = ['Membership Type', 'Name', 'Email']
    for i, header in enumerate(headers):
        ttk.Label(root, text=header).grid(row=0, column=i)

    # Table data
    for i, member in enumerate(student_members):
        print(member)
        member_info = [member[1], member[5], member[6]]
        for j, value in enumerate(member_info):
            # print(value)
            # print(student_members[i][0])
            ttk.Label(root, text=value).grid(row=i+1, column=j)

            # Delete button for each event, delete according to EventID
            ttk.Button(root, text="Delete", command=lambda event_id=student_members[i][0]: delete_member(
                event_id, root)).grid(row=i+1, column=len(headers))

            # Update button for each event, update according to EventID
            ttk.Button(root, text="Update", command=lambda event_id=student_members[i][0]: update_member_window(
                event_id, root)).grid(row=i+1, column=len(headers)+1)


# def membership_management():
#     conn = connect_db()

#     cur.close()
#     conn.close()


def student_management():
    conn = connect_db()

    cur.close()
    conn.close()


def student_membership_management():
    conn = connect_db()

    cur.close()
    conn.close()


def event_registration_management(root):
    for widget in root.winfo_children():
        widget.destroy()
        
    conn = connect_db()
    if conn is None:
        messagebox.showwarning("Connection Failed", "Failed to connect to the database.")
        return

    cur = conn.cursor()
    # Fetch events
    cur.execute("SELECT EventID, EventName, EventDate FROM Event ORDER BY EventDate")
    events = cur.fetchall()

    # Fetch event registrations
    cur.execute("SELECT er.RegistrationID, e.EventName, e.EventDate, er.MembershipID FROM EventRegistration er JOIN Event e ON er.EventID = e.EventID ORDER BY e.EventDate, er.MembershipID")
    registrations = cur.fetchall()
    cur.close()
    conn.close()

    # Create the new window for displaying events and registrations
    event_reg_window = tk.Toplevel()
    event_reg_window.title("Event Registration Management")

    # Section for displaying events
    ttk.Label(event_reg_window, text="Events").grid(row=0, column=0, columnspan=3)
    for i, event in enumerate(events):
        ttk.Label(event_reg_window, text=f"{event[1]} ({event[2]})").grid(row=i+1, column=0)
        ttk.Button(event_reg_window, text="Register", command=lambda event_id=event[0]: register_for_event(event_id, event_reg_window)).grid(row=i+1, column=1)
        ttk.Button(event_reg_window, text="Delete", command=lambda event_id=event[0]: delete_registration_prompt(event_id, event_reg_window, root)).grid(row=i+1, column=2)

    # Visual separation
    ttk.Separator(event_reg_window, orient='horizontal').grid(row=len(events)+2, column=0, columnspan=3, sticky='ew', pady=5)

    # Section for displaying event registrations
    ttk.Label(event_reg_window, text="Event Registrations").grid(row=len(events)+3, column=0, columnspan=3)
    for i, reg in enumerate(registrations):
        ttk.Label(event_reg_window, text=f"{reg[1]} ({reg[2]}), Membership ID: {reg[3]}").grid(row=len(events)+4+i, column=0, columnspan=2)



def create_board_member_window():
    window = tk.Toplevel()
    window.title("Board Member Management")

    # Buttons for different management options
    ttk.Button(window, text="Event Management", command=lambda: event_management(
        window)).grid(column=0, row=0, sticky=tk.W, pady=10)
    ttk.Button(window, text="Membership Management", command=lambda: membership_management(window)).grid(
        column=0, row=1, sticky=tk.W, pady=10)
    ttk.Button(window, text="Student Management", command=student_management).grid(
        column=0, row=2, sticky=tk.W, pady=10)
    ttk.Button(window, text="StudentMembership Management",
               command=student_membership_management).grid(column=0, row=3, sticky=tk.W, pady=10)
    ttk.Button(window, text="EventRegistration Management",
               command=lambda: event_registration_management(window)).grid(column=0, row=4, sticky=tk.W, pady=10)

    # Example function for one of the management options


def verify_membership():
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
                create_board_member_window()

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
ttk.Button(mainframe, text="Login", command=verify_membership).grid(
    column=2, row=2, sticky=tk.W)

# Registration button
ttk.Button(mainframe, text="Register as Member", command=lambda: registration_window(
    root)).grid(column=2, row=3, sticky=tk.W)


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
    inputs = ["Student ID", "Name", "Email",
              "Start Date", "Expire Date", "Membership Type"]
    entries = {}
    for idx, input in enumerate(inputs, start=1):
        ttk.Label(reg_frame, text=input).grid(column=1, row=idx, sticky=tk.W)
        entry_var = tk.StringVar()
        entries[input] = ttk.Entry(reg_frame, width=30, textvariable=entry_var)
        entries[input].grid(column=2, row=idx, sticky=(tk.W, tk.E))

    # Submit button for registration
    ttk.Button(reg_frame, text="Submit", command=lambda: submit_registration(
        entries, reg_win)).grid(column=2, row=len(inputs) + 1, sticky=tk.W)


def submit_registration(entries, window):
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        try:
            # Insert into Student table
            student_id = entries["Student ID"].get()
            name = entries["Name"].get()
            email = entries["Email"].get()
            cur.execute(
                "INSERT INTO Student (StudentID, Name, Email) VALUES (%s, %s, %s)", (student_id, name, email))

            # Generate MembershipID and insert into Membership table
            membership_id = generate_membership_id()
            membership_type = entries["Membership Type"].get()
            start_date = entries["Start Date"].get()
            expire_date = entries["Expire Date"].get()
            cur.execute("INSERT INTO Membership (MembershipID, MembershipType, StartDate, ExpireDate) VALUES (%s, %s, %s, %s)",
                        (membership_id, membership_type, start_date, expire_date))

            # Link Student with Membership in StudentMembership table
            cur.execute("INSERT INTO StudentMembership (StudentID, MembershipID) VALUES (%s, %s)",
                        (student_id, membership_id))

            # Commit the transactions
            conn.commit()

            # Inform the user of successful registration and their MembershipID
            messagebox.showinfo(
                "Registration Successful", f"You are now registered. Your Membership ID is {membership_id}.")
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
