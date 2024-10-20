import tkinter as tk
from tkinter import messagebox
import requests

# Server URL for creating tickets (replace with your server's URL)
SERVER_URL = "http://127.0.0.1:8009/api/tickets"

# Function to submit ticket data to the server
def submit_ticket():
    # Get data from input fields
    title = entry_title.get()
    description = entry_description.get()
    name = entry_name.get()
    office = entry_office.get()
    
    # Validate input fields
    if not title or not description or not name or not office:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    # Create data dictionary
    ticket_data = {
        "title": title,
        "description": description,
        "name": name,
        "office": office
    }

    try:
        # Send POST request to server
        response = requests.post(SERVER_URL, json=ticket_data)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Ticket created successfully!")
            # Clear the form after successful submission
            clear_form()
        else:
            messagebox.showerror("Server Error", "Failed to create ticket. Please try again.")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Could not connect to server. Error: {str(e)}")

# Function to clear the form fields
def clear_form():
    entry_title.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_office.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Ticketing System")

# Set window size
root.geometry("400x300")

# Create a title label
title_label = tk.Label(root, text="Create a New Ticket", font=("Helvetica", 16, "bold"), pady=10)
title_label.pack()

# Create form fields
form_frame = tk.Frame(root, pady=10)
form_frame.pack()

# Title
label_title = tk.Label(form_frame, text="Title:")
label_title.grid(row=0, column=0, sticky=tk.W, pady=5)
entry_title = tk.Entry(form_frame, width=30)
entry_title.grid(row=0, column=1, pady=5)

# Description
label_description = tk.Label(form_frame, text="Description:")
label_description.grid(row=1, column=0, sticky=tk.W, pady=5)
entry_description = tk.Entry(form_frame, width=30)
entry_description.grid(row=1, column=1, pady=5)

# Name
label_name = tk.Label(form_frame, text="Your Name:")
label_name.grid(row=2, column=0, sticky=tk.W, pady=5)
entry_name = tk.Entry(form_frame, width=30)
entry_name.grid(row=2, column=1, pady=5)

# Office
label_office = tk.Label(form_frame, text="Office:")
label_office.grid(row=3, column=0, sticky=tk.W, pady=5)
entry_office = tk.Entry(form_frame, width=30)
entry_office.grid(row=3, column=1, pady=5)

# Submit Button
submit_button = tk.Button(root, text="Create Ticket", command=submit_ticket)
submit_button.pack(pady=10)

# Run the main loop
root.mainloop()
