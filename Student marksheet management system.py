import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error


# ==========================================================
# MYSQL CONNECTION
# ==========================================================

def connect_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="deveshdellg15"
        )

        cursor = connection.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_marksheet")
        cursor.execute("USE student_marksheet")

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)

        # Create students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                roll_no VARCHAR(20) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                student_class VARCHAR(20) NOT NULL,
                division VARCHAR(10),
                english FLOAT NOT NULL,
                maths FLOAT NOT NULL,
                science FLOAT NOT NULL,
                computer FLOAT NOT NULL,
                total FLOAT NOT NULL,
                percentage FLOAT NOT NULL,
                result VARCHAR(20) NOT NULL
            )
        """)

        # Create default login
        cursor.execute(
            "SELECT * FROM users WHERE username = %s",
            ("admin",)
        )

        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                ("admin", "admin123")
            )

        connection.commit()

        return connection

    except Error as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to connect to MySQL.\n\n{e}"
        )
        return None


# ==========================================================
# GLOBAL VARIABLES
# ==========================================================

connection = None
cursor = None

root = tk.Tk()
root.title("Student Marksheet Management System")
root.geometry("1100x700")
root.resizable(False, False)

main_frame = None


# ==========================================================
# LOGIN PAGE
# ==========================================================

def login_page():

    global main_frame

    for widget in root.winfo_children():
        widget.destroy()

    login_frame = tk.Frame(root)
    login_frame.pack(expand=True)

    title = tk.Label(
        login_frame,
        text="STUDENT MARKSHEET MANAGEMENT SYSTEM",
        font=("Arial", 22, "bold")
    )
    title.grid(row=0, column=0, columnspan=2, pady=30)

    tk.Label(
        login_frame,
        text="Login",
        font=("Arial", 20, "bold")
    ).grid(row=1, column=0, columnspan=2, pady=15)

    tk.Label(
        login_frame,
        text="Username",
        font=("Arial", 12)
    ).grid(row=2, column=0, padx=10, pady=10, sticky="e")

    username_entry = tk.Entry(
        login_frame,
        width=30,
        font=("Arial", 12)
    )
    username_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(
        login_frame,
        text="Password",
        font=("Arial", 12)
    ).grid(row=3, column=0, padx=10, pady=10, sticky="e")

    password_entry = tk.Entry(
        login_frame,
        width=30,
        show="*",
        font=("Arial", 12)
    )
    password_entry.grid(row=3, column=1, padx=10, pady=10)

    def check_login():

        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == "" or password == "":
            messagebox.showwarning(
                "Validation",
                "Please enter username and password."
            )
            return

        try:
            cursor.execute(
                """
                SELECT * FROM users
                WHERE username = %s AND password = %s
                """,
                (username, password)
            )

            user = cursor.fetchone()

            if user:
                dashboard()
            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )

        except Error as e:
            messagebox.showerror("Error", str(e))

    tk.Button(
        login_frame,
        text="LOGIN",
        width=15,
        font=("Arial", 12, "bold"),
        command=check_login
    ).grid(row=4, column=0, columnspan=2, pady=20)

    tk.Label(
        login_frame,
        text="Default Login: admin / admin123",
        font=("Arial", 10)
    ).grid(row=5, column=0, columnspan=2)


# ==========================================================
# DASHBOARD
# ==========================================================

def dashboard():

    global main_frame

    for widget in root.winfo_children():
        widget.destroy()

    # Heading
    tk.Label(
        root,
        text="STUDENT MARKSHEET MANAGEMENT SYSTEM",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    tk.Label(
        root,
        text="Dashboard",
        font=("Arial", 18)
    ).pack(pady=5)

    main_frame = tk.Frame(root)
    main_frame.pack(pady=30)

    tk.Button(
        main_frame,
        text="Add Student",
        width=20,
        height=2,
        command=add_student
    ).grid(row=0, column=0, padx=15, pady=15)

    tk.Button(
        main_frame,
        text="View Records",
        width=20,
        height=2,
        command=view_students
    ).grid(row=0, column=1, padx=15, pady=15)

    tk.Button(
        main_frame,
        text="Search Student",
        width=20,
        height=2,
        command=search_student
    ).grid(row=1, column=0, padx=15, pady=15)

    tk.Button(
        main_frame,
        text="Update Student",
        width=20,
        height=2,
        command=update_student
    ).grid(row=1, column=1, padx=15, pady=15)

    tk.Button(
        main_frame,
        text="Delete Student",
        width=20,
        height=2,
        command=delete_student
    ).grid(row=2, column=0, padx=15, pady=15)

    tk.Button(
        main_frame,
        text="Logout",
        width=20,
        height=2,
        command=logout
    ).grid(row=2, column=1, padx=15, pady=15)


# ==========================================================
# ADD STUDENT
# ==========================================================

def add_student():

    window = tk.Toplevel(root)
    window.title("Add Student")
    window.geometry("600x650")
    window.resizable(False, False)

    tk.Label(
        window,
        text="ADD STUDENT RECORD",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    form = tk.Frame(window)
    form.pack()

    labels = [
        "Roll No",
        "Name",
        "Class",
        "Division",
        "English Marks",
        "Maths Marks",
        "Science Marks",
        "Computer Marks"
    ]

    entries = []

    for i, label in enumerate(labels):

        tk.Label(
            form,
            text=label,
            font=("Arial", 11)
        ).grid(row=i, column=0, padx=10, pady=8, sticky="e")

        entry = tk.Entry(
            form,
            width=30,
            font=("Arial", 11)
        )
        entry.grid(row=i, column=1, padx=10, pady=8)

        entries.append(entry)

    def save_student():

        roll = entries[0].get().strip()
        name = entries[1].get().strip()
        student_class = entries[2].get().strip()
        division = entries[3].get().strip()

        try:
            english = float(entries[4].get())
            maths = float(entries[5].get())
            science = float(entries[6].get())
            computer = float(entries[7].get())

        except ValueError:
            messagebox.showerror(
                "Invalid Marks",
                "Please enter valid numbers for all marks."
            )
            return

        # Basic validation
        if roll == "" or name == "" or student_class == "":
            messagebox.showwarning(
                "Validation",
                "Please fill all required fields."
            )
            return

        marks = [english, maths, science, computer]

        for mark in marks:
            if mark < 0 or mark > 100:
                messagebox.showerror(
                    "Invalid Marks",
                    "Marks must be between 0 and 100."
                )
                return

        try:

            cursor.execute(
                "SELECT * FROM students WHERE roll_no = %s",
                (roll,)
            )

            if cursor.fetchone():
                messagebox.showerror(
                    "Duplicate Roll No",
                    "A student with this roll number already exists."
                )
                return

            total = sum(marks)
            percentage = total / 4

            if all(mark >= 35 for mark in marks):
                result = "PASS"
            else:
                result = "FAIL"

            cursor.execute(
                """
                INSERT INTO students
                (roll_no, name, student_class, division,
                 english, maths, science, computer,
                 total, percentage, result)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s)
                """,
                (
                    roll,
                    name,
                    student_class,
                    division,
                    english,
                    maths,
                    science,
                    computer,
                    total,
                    percentage,
                    result
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Student record added successfully."
            )

            clear_entries(entries)

        except Error as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        window,
        text="SAVE",
        width=15,
        command=save_student
    ).pack(pady=15)

    tk.Button(
        window,
        text="CLEAR",
        width=15,
        command=lambda: clear_entries(entries)
    ).pack()


# ==========================================================
# CLEAR FIELDS
# ==========================================================

def clear_entries(entries):

    for entry in entries:
        entry.delete(0, tk.END)


# ==========================================================
# VIEW STUDENTS
# ==========================================================

def view_students():

    window = tk.Toplevel(root)
    window.title("View Student Records")
    window.geometry("1100x550")

    tk.Label(
        window,
        text="STUDENT RECORDS",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    table_frame = tk.Frame(window)
    table_frame.pack(fill="both", expand=True)

    columns = (
        "ID",
        "Roll No",
        "Name",
        "Class",
        "Division",
        "English",
        "Maths",
        "Science",
        "Computer",
        "Total",
        "Percentage",
        "Result"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=85,
            anchor="center"
        )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    try:

        cursor.execute(
            "SELECT * FROM students ORDER BY id"
        )

        records = cursor.fetchall()

        for record in records:

            tree.insert(
                "",
                tk.END,
                values=record
            )

    except Error as e:
        messagebox.showerror("Error", str(e))


# ==========================================================
# SEARCH STUDENT
# ==========================================================

def search_student():

    window = tk.Toplevel(root)
    window.title("Search Student")
    window.geometry("1000x550")

    tk.Label(
        window,
        text="SEARCH STUDENT",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    search_frame = tk.Frame(window)
    search_frame.pack(pady=10)

    tk.Label(
        search_frame,
        text="Enter Roll No:",
        font=("Arial", 12)
    ).pack(side="left", padx=10)

    search_entry = tk.Entry(
        search_frame,
        width=25
    )
    search_entry.pack(side="left", padx=10)

    columns = (
        "ID",
        "Roll No",
        "Name",
        "Class",
        "Division",
        "English",
        "Maths",
        "Science",
        "Computer",
        "Total",
        "Percentage",
        "Result"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=80,
            anchor="center"
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    def search():

        for item in tree.get_children():
            tree.delete(item)

        roll = search_entry.get().strip()

        if roll == "":
            messagebox.showwarning(
                "Search",
                "Please enter a roll number."
            )
            return

        try:

            cursor.execute(
                "SELECT * FROM students WHERE roll_no = %s",
                (roll,)
            )

            record = cursor.fetchone()

            if record:

                tree.insert(
                    "",
                    tk.END,
                    values=record
                )

            else:

                messagebox.showinfo(
                    "Not Found",
                    "No student found with this roll number."
                )

        except Error as e:
            messagebox.showerror("Error", str(e))

    tk.Button(
        search_frame,
        text="SEARCH",
        command=search
    ).pack(side="left")


# ==========================================================
# UPDATE STUDENT
# ==========================================================

def update_student():

    window = tk.Toplevel(root)
    window.title("Update Student")
    window.geometry("600x650")

    tk.Label(
        window,
        text="UPDATE STUDENT RECORD",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    form = tk.Frame(window)
    form.pack()

    labels = [
        "Roll No",
        "Name",
        "Class",
        "Division",
        "English Marks",
        "Maths Marks",
        "Science Marks",
        "Computer Marks"
    ]

    entries = []

    for i, label in enumerate(labels):

        tk.Label(
            form,
            text=label
        ).grid(
            row=i,
            column=0,
            padx=10,
            pady=8,
            sticky="e"
        )

        entry = tk.Entry(
            form,
            width=30
        )

        entry.grid(
            row=i,
            column=1,
            padx=10,
            pady=8
        )

        entries.append(entry)

    def load_student():

        roll = entries[0].get().strip()

        if roll == "":
            messagebox.showwarning(
                "Validation",
                "Enter Roll No first."
            )
            return

        try:

            cursor.execute(
                "SELECT * FROM students WHERE roll_no = %s",
                (roll,)
            )

            record = cursor.fetchone()

            if record is None:
                messagebox.showerror(
                    "Not Found",
                    "Student record not found."
                )
                return

            # record indexes
            entries[1].delete(0, tk.END)
            entries[1].insert(0, record[2])

            entries[2].delete(0, tk.END)
            entries[2].insert(0, record[3])

            entries[3].delete(0, tk.END)
            entries[3].insert(0, record[4])

            entries[4].delete(0, tk.END)
            entries[4].insert(0, record[5])

            entries[5].delete(0, tk.END)
            entries[5].insert(0, record[6])

            entries[6].delete(0, tk.END)
            entries[6].insert(0, record[7])

            entries[7].delete(0, tk.END)
            entries[7].insert(0, record[8])

        except Error as e:
            messagebox.showerror("Error", str(e))

    def update_record():

        roll = entries[0].get().strip()
        name = entries[1].get().strip()
        student_class = entries[2].get().strip()
        division = entries[3].get().strip()

        if roll == "" or name == "" or student_class == "":
            messagebox.showwarning(
                "Validation",
                "Please fill required fields."
            )
            return

        try:

            english = float(entries[4].get())
            maths = float(entries[5].get())
            science = float(entries[6].get())
            computer = float(entries[7].get())

        except ValueError:
            messagebox.showerror(
                "Invalid Marks",
                "Enter valid marks."
            )
            return

        marks = [
            english,
            maths,
            science,
            computer
        ]

        if any(mark < 0 or mark > 100 for mark in marks):
            messagebox.showerror(
                "Invalid Marks",
                "Marks must be between 0 and 100."
            )
            return

        total = sum(marks)
        percentage = total / 4

        if all(mark >= 35 for mark in marks):
            result = "PASS"
        else:
            result = "FAIL"

        try:

            cursor.execute(
                """
                UPDATE students
                SET name=%s,
                    student_class=%s,
                    division=%s,
                    english=%s,
                    maths=%s,
                    science=%s,
                    computer=%s,
                    total=%s,
                    percentage=%s,
                    result=%s
                WHERE roll_no=%s
                """,
                (
                    name,
                    student_class,
                    division,
                    english,
                    maths,
                    science,
                    computer,
                    total,
                    percentage,
                    result,
                    roll
                )
            )

            connection.commit()

            if cursor.rowcount == 0:
                messagebox.showerror(
                    "Error",
                    "Student record not found."
                )
            else:
                messagebox.showinfo(
                    "Success",
                    "Student record updated successfully."
                )

        except Error as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        window,
        text="LOAD RECORD",
        width=15,
        command=load_student
    ).pack(pady=10)

    tk.Button(
        window,
        text="UPDATE",
        width=15,
        command=update_record
    ).pack(pady=10)

    tk.Button(
        window,
        text="CLEAR",
        width=15,
        command=lambda: clear_entries(entries)
    ).pack(pady=5)


# ==========================================================
# DELETE STUDENT
# ==========================================================

def delete_student():

    window = tk.Toplevel(root)
    window.title("Delete Student")
    window.geometry("400x250")
    window.resizable(False, False)

    tk.Label(
        window,
        text="DELETE STUDENT",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

    tk.Label(
        window,
        text="Enter Roll No:"
    ).pack(pady=5)

    roll_entry = tk.Entry(
        window,
        width=30
    )
    roll_entry.pack(pady=5)

    def delete_record():

        roll = roll_entry.get().strip()

        if roll == "":
            messagebox.showwarning(
                "Validation",
                "Please enter Roll No."
            )
            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this record?"
        )

        if not answer:
            return

        try:

            cursor.execute(
                "DELETE FROM students WHERE roll_no = %s",
                (roll,)
            )

            connection.commit()

            if cursor.rowcount > 0:

                messagebox.showinfo(
                    "Success",
                    "Student record deleted successfully."
                )

                roll_entry.delete(0, tk.END)

            else:

                messagebox.showerror(
                    "Not Found",
                    "Student record not found."
                )

        except Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        window,
        text="DELETE",
        width=15,
        command=delete_record
    ).pack(pady=20)


# ==========================================================
# LOGOUT
# ==========================================================

def logout():

    answer = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if answer:
        login_page()


# ==========================================================
# PROGRAM START
# ==========================================================

connection = connect_database()

if connection:

    cursor = connection.cursor()

    login_page()

    root.mainloop()

    cursor.close()
    connection.close()

else:

    root.destroy()
