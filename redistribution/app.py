from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Email Configuration (FastMail)
app.config['MAIL_SERVER'] = 'smtp.fastmail.com'  # FastMail SMTP server
app.config['MAIL_PORT'] = 465  # SSL-enabled port
app.config['MAIL_USE_TLS'] = False  # Use SSL instead of TLS
app.config['MAIL_USE_SSL'] = True  # Use SSL for secure connection
app.config['MAIL_USERNAME'] = 'nocrumbs@fastmail.com'  # Your FastMail email address
app.config['MAIL_PASSWORD'] = '6y3y7h8j2z2x2a4q'  # Your FastMail app password
app.config['MAIL_DEFAULT_SENDER'] = 'nocrumbs@fastmail.com'  # Default sender for all emails
mail = Mail(app)

# Define User and Donation Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)  # 'donor' or 'ngo'

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    donor = db.relationship('User', back_populates="donations")

User.donations = db.relationship('Donation', back_populates='donor')

# Initialize the database (Run once)
@app.before_first_request
def create_tables():
    db.create_all()

# Home Route - Simple landing page
@app.route('/')
def home():
    return render_template('index.html')

# Route for registering a donor or NGO
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "User registered successfully!"}), 201

# Route for posting a donation
@app.route('/donate', methods=['POST'])
def donate():
    data = request.get_json()
    donor = User.query.filter_by(email=data['donor_email']).first()
    if donor and donor.role == 'donor':
        new_donation = Donation(
            food_type=data['food_type'],
            quantity=data['quantity'],
            expiration_date=data['expiration_date'],
            description=data.get('description', ''),
            donor_id=donor.id
        )
        db.session.add(new_donation)
        db.session.commit()
        return jsonify({"status": "Donation posted successfully!"}), 201
    return jsonify({"error": "Invalid donor or donor not registered"}), 400

# Route to get all available donations for NGOs
@app.route('/donations', methods=['GET'])
def get_donations():
    donations = Donation.query.all()
    donations_data = [{"id": d.id, "food_type": d.food_type, "quantity": d.quantity, "expiration_date": d.expiration_date, "description": d.description} for d in donations]
    return jsonify(donations_data), 200

# Route to request a donation
@app.route('/request_donation', methods=['POST'])
def request_donation():
    data = request.get_json()
    ngo_email = data.get('ngo_email')
    donation_id = data.get('donation_id')

    if not ngo_email or not donation_id:
        return jsonify({"error": "NGO email and Donation ID are required"}), 400

    ngo = User.query.filter_by(email=ngo_email, role='ngo').first()
    if ngo:
        donation = Donation.query.get(donation_id)  # Query the database using the donation_id
        if donation:
            # Get the donor's email address
            donor = User.query.get(donation.donor_id)
            donor_email = donor.email

            # Send email from NGO to Donor
            subject = f"Donation Request for {donation.food_type}"
            body = f"""
            Dear Donor,

            An NGO with the email {ngo_email} has requested your donation of {donation.food_type}.
            Here are the details of the donation:

            Food Type: {donation.food_type}
            Quantity: {donation.quantity}
            Expiration Date: {donation.expiration_date}
            Description: {donation.description}

            Please respond to this request if you are willing to donate.

            Best regards,
            Food Redistribution Platform
            """

            # Specify sender explicitly, even though we have a default sender
            msg = Message(subject=subject, recipients=[donor_email], sender='nocrumbs@fastmail.com')
            msg.body = body

            try: 
                # Send the email
                mail.send(msg)
                return jsonify({"status": "Donation request sent and email sent to the donor!"}), 200
            except Exception as e:
                return jsonify({"error": f"Failed to send email: {str(e)}"}), 500
        else:
            return jsonify({"error": "Donation not found"}), 404
    else:
        return jsonify({"error": "Invalid NGO or NGO not registered"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
