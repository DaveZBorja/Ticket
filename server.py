from flask import Flask, jsonify, request, render_template, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-interactive plotting
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Set a secret key for sessions
db = SQLAlchemy(app)

# Allow cross-origin requests
CORS(app)

# Define the Ticket model
class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='Open', nullable=False)
    name = db.Column(db.String, nullable=False)
    office = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'name': self.name,
            'office': self.office,
            'created_at': self.created_at.isoformat(),
            'deleted': self.deleted
        }

# Define a TicketAction model to track history and actions taken on each ticket
class TicketAction(db.Model):
    __tablename__ = 'ticket_action'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    action_type = db.Column(db.String, nullable=False)
    action_description = db.Column(db.String, nullable=False)
    action_time = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'action_type': self.action_type,
            'action_description': self.action_description,
            'action_time': self.action_time.isoformat()
        }

# Define the Admin model for user authentication
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize the database and create the admin user if not exists
with app.app_context():
    db.create_all()
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        hashed_password = generate_password_hash('admin123')
        admin = Admin(username='admin', password=hashed_password)
        db.session.add(admin)
        db.session.commit()
    else:
        if not check_password_hash(admin.password, 'admin123'):
            admin.password = generate_password_hash('admin123')
            db.session.commit()

# Route to retrieve all tickets
@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    tickets = Ticket.query.filter_by(deleted=False).order_by(Ticket.created_at.desc()).all()
    return jsonify([ticket.to_dict() for ticket in tickets])

# Route to create a new ticket
@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    data = request.json
    new_ticket = Ticket(
        title=data['title'],
        description=data['description'],
        name=data['name'],
        office=data['office'],
        created_at=datetime.utcnow()
    )
    db.session.add(new_ticket)
    db.session.commit()

    # Create a new action log entry
    new_action = TicketAction(
        ticket_id=new_ticket.id,
        action_type='Created',
        action_description=f"Ticket '{new_ticket.title}' was created by {new_ticket.name}.",
        action_time=datetime.utcnow()
    )
    db.session.add(new_action)
    db.session.commit()

    return jsonify(new_ticket.to_dict()), 201

# Route to update a ticket's status
@app.route('/api/tickets/<int:id>', methods=['PUT'])
def update_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    data = request.json
    old_status = ticket.status
    ticket.status = data['status']
    db.session.commit()

    # Log the status update in the action log
    new_action = TicketAction(
        ticket_id=id,
        action_type='Status Update',
        action_description=f"Status changed from {old_status} to {ticket.status}.",
        action_time=datetime.utcnow()
    )
    db.session.add(new_action)
    db.session.commit()

    return jsonify(ticket.to_dict())

# Route to get the action history for a specific ticket
@app.route('/api/tickets/<int:id>/history', methods=['GET'])
def get_ticket_history(id):
    Ticket.query.get_or_404(id)  # Ensure ticket exists
    actions = TicketAction.query.filter_by(ticket_id=id).order_by(TicketAction.action_time.asc()).all()
    return jsonify([action.to_dict() for action in actions])

# Route to delete a ticket (soft delete)
@app.route('/api/tickets/<int:id>', methods=['DELETE'])
def delete_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    ticket.deleted = True
    db.session.commit()

    # Log the deletion in the action log
    new_action = TicketAction(
        ticket_id=id,
        action_type='Deletion',
        action_description=f"Ticket '{ticket.title}' was deleted.",
        action_time=datetime.utcnow()
    )
    db.session.add(new_action)
    db.session.commit()

    return '', 204

# Route to export tickets to CSV
@app.route('/admin/export', methods=['GET'])
def export_tickets():
    tickets = Ticket.query.filter_by(deleted=False).all()
    
    # Prepare data for CSV export
    tickets_data = []
    for ticket in tickets:
        tickets_data.append({
            'ID': ticket.id,
            'Title': ticket.title,
            'Description': ticket.description,
            'Status': ticket.status,
            'Name': ticket.name,
            'Created At': ticket.created_at.isoformat(),
        })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(tickets_data)
    csv_file_path = os.path.join('/home/mint/Desktop/Tickets/', 'tickets.csv')
    df.to_csv(csv_file_path, index=False)

    # Send the CSV file
    return send_file(csv_file_path, as_attachment=True, mimetype='text/csv')

# Route to handle admin login
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    admin = Admin.query.filter_by(username=data['username']).first()
    if admin and check_password_hash(admin.password, data['password']):
        session['admin_id'] = admin.id
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Route to handle admin logout
@app.route('/admin/logout', methods=['POST', 'GET'])
def admin_logout():
    session.pop('admin_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

# Route to check admin session and render admin panel
@app.route('/admin', methods=['GET'])
def admin_panel():
    if 'admin_id' in session:
        tickets = Ticket.query.filter_by(deleted=False).order_by(Ticket.created_at.desc()).all()  # Sort by created_at descending
        return render_template('admin_panel.html', tickets=tickets)
    return redirect(url_for('login_page'))

# Route for plotting ticket titles
@app.route('/admin/plot_titles', methods=['GET'])
def plot_ticket_titles():
    tickets = Ticket.query.filter_by(deleted=False).all()
    titles = [ticket.title for ticket in tickets]
    title_counts = pd.Series(titles).value_counts()

    # Create the plot
    plt.figure(figsize=(10, 5))
    title_counts.plot(kind='bar', color='skyblue')
    plt.title('Ticket Title Frequency')
    plt.xlabel('Ticket Titles')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Encode the image to base64
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('plot.html', plot_url=plot_url)

# Serve login page for admin
@app.route('/admin/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Route for creating a ticket (front-end)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8009)

