import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt


# Create the expenses table in the database
def create_table():
    conn.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "amount REAL, category TEXT, date TEXT, description TEXT)")
    conn.commit()


# Insert a new expense into the database
def insert_expense(amount, category, date, description):
    conn.execute("INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
                 (amount, category, date, description))
    conn.commit()


# Generate a report of expenses by category
def generate_report():
    cursor = conn.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    categories = []
    amounts = []
    for row in cursor:
        categories.append(row[0])
        amounts.append(row[1])
    if len(categories) == 0:
        messagebox.showinfo("Report", "No expenses found.")
    else:
        plt.bar(categories, amounts)
        plt.xlabel("Categories")
        plt.ylabel("Total Amount")
        plt.title("Expense Report")
        plt.show()


# Submit button action
def submit_expense():
    amount = amount_entry.get()
    category = category_entry.get()
    date = date_entry.get()
    description = description_entry.get()

    if amount and category and date:
        insert_expense(amount, category, date, description)
        messagebox.showinfo("Expense Tracker", "Expense added successfully.")
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Expense Tracker", "Please fill in all the fields.")


# Generate report button action
def show_report():
    generate_report()


# Create the main window
window = tk.Tk()
window.title("Expense Tracker")

# Create labels and entry fields
amount_label = tk.Label(window, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(window)
amount_entry.pack()

category_label = tk.Label(window, text="Category:")
category_label.pack()
category_entry = tk.Entry(window)
category_entry.pack()

date_label = tk.Label(window, text="Date:")
date_label.pack()
date_entry = tk.Entry(window)
date_entry.pack()

description_label = tk.Label(window, text="Description:")
description_label.pack()
description_entry = tk.Entry(window)
description_entry.pack()

# Create submit and report buttons
submit_button = tk.Button(window, text="Submit", command=submit_expense)
submit_button.pack()

report_button = tk.Button(window, text="Generate Report", command=show_report)
report_button.pack()

# Connect to the database
conn = sqlite3.connect("expenses.db")
create_table()

# Start the main loop
window.mainloop()

# Close the database connection
conn.close()
