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
root.title("Ticketing System")

# Set window size and background color
root.geometry("500x400")
root.configure(bg="#f0f0f0")

# Define font styles
header_font = ("Helvetica", 16, "bold")
label_font = ("Arial", 12)
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# Create header frame
header_frame = tk.Frame(root, bg="#4CAF50", pady=10)
header_frame.pack(fill="x")

# Header Label
header_label = tk.Label(header_frame, text="Create a New Ticket", font=header_font, fg="white", bg="#4CAF50")
header_label.pack()

# Create form frame for better layout control
form_frame = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
form_frame.pack()

# Create input fields with labels for the ticket form
tk.Label(form_frame, text="Title:", font=label_font, bg="#f0f0f0").grid(row=0, column=0, sticky="e", pady=5)
entry_title = tk.Entry(form_frame, font=entry_font, width=30)
entry_title.grid(row=0, column=1, pady=5, padx=5)

tk.Label(form_frame, text="Description:", font=label_font, bg="#f0f0f0").grid(row=1, column=0, sticky="e", pady=5)
entry_description = tk.Entry(form_frame, font=entry_font, width=30)
entry_description.grid(row=1, column=1, pady=5, padx=5)

tk.Label(form_frame, text="Name:", font=label_font, bg="#f0f0f0").grid(row=2, column=0, sticky="e", pady=5)
entry_name = tk.Entry(form_frame, font=entry_font, width=30)
entry_name.grid(row=2, column=1, pady=5, padx=5)

tk.Label(form_frame, text="Office:", font=label_font, bg="#f0f0f0").grid(row=3, column=0, sticky="e", pady=5)
entry_office = tk.Entry(form_frame, font=entry_font, width=30)
entry_office.grid(row=3, column=1, pady=5, padx=5)

# Create the submit button with styling
submit_button = tk.Button(root, text="Submit Ticket", font=button_font, bg="#4a7abc", fg="white", command=submit_ticket)
submit_button.pack(pady=20)

# Start the main event loop
root.mainloop()
