from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'  # Change this to MySQL or PostgreSQL as needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Models
class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Employer {self.name}>"

from datetime import datetime

class JobListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)

    employer = db.relationship('Employer', backref=db.backref('job_listings', lazy=True))

    def __repr__(self):
        return f'<JobListing {self.title}>'

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    resume = db.Column(db.String(100), nullable=False)

class StatusUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)
    job_listing_id = db.Column(db.Integer, db.ForeignKey('job_listing.id'), nullable=False)
    job_listing = db.relationship('JobListing', backref='status_updates')


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_employer', methods=['GET', 'POST'])
def add_employer():
    if request.method == 'POST':
        employer_name = request.form['employer_name']
        employer_email = request.form['employer_email']

        # Check if the employer already exists in the database
        existing_employer = Employer.query.filter_by(email=employer_email).first()
        if existing_employer:
            flash('Employer with this email already exists', 'error')
            return redirect(url_for('add_employer'))

        # Create and add the new employer
        new_employer = Employer(name=employer_name, email=employer_email)
        db.session.add(new_employer)
        db.session.commit()

        flash('Employer added successfully', 'success')
        return redirect(url_for('add_job_listing'))  # Redirect to add job listing page

    return render_template('add_employer.html')


@app.route('/add_job_listing', methods=['GET', 'POST'])
def add_job_listing():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        employer_id = request.form.get('employer_id')  # Get the employer_id from the form

        # Example validation logic (make sure all fields are provided)
        if title and description and employer_id:
            employer = Employer.query.get(employer_id)  # Fetch employer by ID
            if employer:
                new_job = JobListing(title=title, description=description, employer_id=employer.id)
                db.session.add(new_job)
                db.session.commit()
                message = "Job listing added successfully!"
            else:
                message = "Employer not found."
        else:
            message = "Please fill in all fields."

        return render_template('add_job_listing.html', message=message)

    # Retrieve all employers to show in the dropdown
    employers = Employer.query.all()
    return render_template('add_job_listing.html', employers=employers)


@app.route('/delete_job_listing/<int:id>', methods=['POST'])
def delete_job_listing(id):
    job_listing = JobListing.query.get(id)
    if job_listing:
        db.session.delete(job_listing)
        db.session.commit()
        return redirect(url_for('job_listings'))  # Redirect to the job listings page
    return "Job listing not found", 404

@app.route('/candidates')
def candidates():
    candidates = Candidate.query.all()
    return render_template('candidates.html', candidates=candidates)

# Route for viewing job listings
@app.route('/job_listings')
def job_listings():
    listings = JobListing.query.all()
    return render_template('job_listings.html', listings=listings)

@app.route('/status_updates')
def status_updates():
    status_updates = StatusUpdate.query.all()
    return render_template('status_updates.html', status_updates=status_updates)




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from environment or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)  # Bind to 0.0.0.0

