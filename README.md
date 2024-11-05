Ticketing System

This is a web-based and Tkinter-based Ticketing System designed to streamline ticket management. It allows users to create and manage tickets for various issues or requests, with an admin panel for viewing and controlling the tickets.
Features

    Create Tickets: Users can create new tickets with details such as title, description, name, and office.
    Admin Panel: Admins can view, update, and delete tickets, as well as export ticket data to CSV.
    Real-Time Updates: Newly created tickets appear at the top of the list.
    Search and Filter: Easily find specific tickets based on various criteria.
    Desktop Application: A Tkinter-based desktop app allows users to submit tickets to the server.
    API Integration: The system uses a RESTful API to manage tickets.

Project Structure

plaintext

TicketingSystem/
├── static/
│   ├── styles.css        # CSS file for styling the web pages
│   └── logo.png          # Logo image file (if applicable)
├── templates/
│   ├── create_ticket.html   # HTML template for creating a new ticket
│   ├── admin_panel.html     # HTML template for the admin panel
├── server.py             # Main Flask application file
├── api.py                # RESTful API for handling ticket operations
├── Tkinter/
│   ├── ticketv3.py       # Tkinter-based application for ticket submission
│   ├── logo.png          # Small logo used in the Tkinter app
├── requirements.txt      # List of required Python packages
└── README.md             # Project documentation

Getting Started
Prerequisites

Ensure that the following software is installed on your system:

    Python 3.x
    Flask
    Tkinter
    Pillow (for image handling in Tkinter)

Installation

    Clone this repository:

    bash

git clone https://github.com/DaveZBorja/Ticket.git

Navigate to the project directory:

bash

cd ticketing-system

Install the required dependencies:

bash

pip install -r requirements.txt

Set up the Flask server by running:

bash

python server.py

For the Tkinter application, navigate to the Tkinter directory:

bash

cd Tkinter

Run the Tkinter application:

bash

    python ticketv3.py

Running the Web Application

    Start the Flask server:

    bash

python server.py

Open your web browser and navigate to:

arduino

http://127.0.0.1:5000

You should see the "Create Ticket" page. Fill in the required details and submit a new ticket.

To access the admin panel, navigate to:

    http://127.0.0.1:5000/admin

Using the Tkinter Desktop Application

    Run the Tkinter application:

    bash

    python Tkinter/ticketv3.py

    Enter the required ticket information in the provided fields and click "Submit" to send the ticket to the server.

REST API Endpoints
Create a New Ticket

    Endpoint: /api/tickets

    Method: POST

    Request Body:

    json

    {
      "title": "Issue Title",
      "description": "Description of the issue",
      "name": "User's Name",
      "office": "User's Office"
    }

    Response: 201 Created if successful.

Get All Tickets

    Endpoint: /api/tickets
    Method: GET
    Response: A list of all existing tickets.

Update Ticket Status

    Endpoint: /api/tickets/<ticket_id>

    Method: PUT

    Request Body:

    json

    {
      "status": "New Status"
    }

    Response: 200 OK if successful.

Delete a Ticket

    Endpoint: /api/tickets/<ticket_id>
    Method: DELETE
    Response: 200 OK if successful.

Screenshots
Create a New Ticket

Admin Panel

Troubleshooting

    Issue: Unable to create a ticket from Tkinter app.
        Solution: Ensure the Flask server is running and the API endpoint is accessible.

    Issue: ImportError for ImageTk in the Tkinter app.
        Solution: Make sure Pillow is installed correctly. Reinstall using pip install pillow.

Contributing

Feel free to fork this repository and submit pull requests with new features or bug fixes. Please make sure to follow the project's coding standards and include relevant documentation.
License

This project is licensed under the MIT License. See the LICENSE file for more details.


