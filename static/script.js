
// Fetch all tickets when the page loads
window.onload = function() {
    getTickets();
};

// Function to create a new ticket
function createTicket() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;

    if (title && description) {
        fetch('/api/tickets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: title, description: description })
        })
        .then(response => response.json())
        .then(data => {
            alert('Ticket created successfully!');
            getTickets(); // Refresh the ticket list
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please fill in both title and description.');
    }
}

// Function to fetch and display all tickets
function getTickets() {
    fetch('/api/tickets')
    .then(response => response.json())
    .then(tickets => {
        const ticketsContainer = document.getElementById('tickets-container');
        ticketsContainer.innerHTML = '';

        tickets.forEach(ticket => {
            const ticketElement = document.createElement('div');
            ticketElement.className = 'ticket';
            ticketElement.innerHTML = `
                <h3>${ticket.title}</h3>
                <p>${ticket.description}</p>
                <p>Status: ${ticket.status}</p>
            `;
            ticketsContainer.appendChild(ticketElement);
        });
    })
    .catch(error => console.error('Error:', error));
}
