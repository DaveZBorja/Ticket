import requests
import tkinter as tk
from tkinter import messagebox

# Define the server URL
SERVER_URL = "http://127.0.0.1:8009/api/tickets"

# Function to submit ticket data to the server
def submit_ticket():
    title = entry_title.get()
    description = entry_description.get()
    name = entry_name.get()
    office = entry_office.get()

    # Validate that all fields are filled
    if not title or not description or not name or not office:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    # Create the ticket data to send
    ticket_data = {
        "title": title,
        "description": description,
        "name": name,
        "office": office
    }

    try:
        # Send POST request to the server
        response = requests.post(SERVER_URL, json=ticket_data)

        # Debugging output
        print(f"Response Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        # Check the response status code and handle accordingly
        if response.status_code == 201:  # 201 indicates the ticket was successfully created
            messagebox.showinfo("Success", "Ticket created successfully!")
            clear_form()  # Optional: Clear the form fields after submission
        else:
            messagebox.showerror("Server Error", f"Failed to create ticket: {response.text}")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Could not connect to server. Error: {str(e)}")

# Function to clear form fields after successful submission
def clear_form():
    entry_title.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_office.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Create Ticket")

# Create input fields for the ticket form
tk.Label(root, text="Title:").grid(row=0, column=0)
entry_title = tk.Entry(root)
entry_title.grid(row=0, column=1)

tk.Label(root, text="Description:").grid(row=1, column=0)
entry_description = tk.Entry(root)
entry_description.grid(row=1, column=1)

tk.Label(root, text="Name:").grid(row=2, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=2, column=1)

tk.Label(root, text="Office:").grid(row=3, column=0)
entry_office = tk.Entry(root)
entry_office.grid(row=3, column=1)

# Create the submit button
submit_button = tk.Button(root, text="Submit Ticket", command=submit_ticket)
submit_button.grid(row=4, columnspan=2)

# Start the main event loop
root.mainloop()
