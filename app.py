from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')  # Use environment variable for DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Use environment variable for secret key

# Initialize database and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True, unique=True)

    def __repr__(self):
        return f"<Employer {self.name}>"

class JobListing(db.Model):
    __tablename__ = 'job_listing'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)

    employer = db.relationship('Employer', backref=db.backref('job_listings', lazy=True))

    def __repr__(self):
        return f"<JobListing {self.title}>"

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    skills = db.Column(db.Text, nullable=True)
    resume_link = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.Text, nullable=True)
    job_preferences = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Candidate {self.name}>"

class JobStatusUpdate(db.Model):
    __tablename__ = 'job_status_updates'
    status_update_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_listing.id'), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job_listing = db.relationship('JobListing', backref=db.backref('status_updates', lazy=True))

    def __repr__(self):
        return f"<JobStatusUpdate {self.status_update_id}, Status {self.status}>"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_listing_id = db.Column(db.Integer, db.ForeignKey('job_listing.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    candidate = db.relationship('Candidate', backref=db.backref('applications', lazy=True))
    job_listing = db.relationship('JobListing', backref=db.backref('applications', lazy=True))

    def __repr__(self):
        return f"<Application {self.id}, Candidate {self.candidate_id}, JobListing {self.job_listing_id}>"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_employer', methods=['GET', 'POST'])
def add_employer():
    if request.method == 'POST':
        employer_name = request.form['employer_name']
        employer_email = request.form['employer_email']

        if Employer.query.filter_by(email=employer_email).first():
            flash('Employer with this email already exists.', 'error')
        elif not employer_name or not employer_email:
            flash('Please fill in all fields.', 'error')
        else:
            new_employer = Employer(name=employer_name, email=employer_email)
            db.session.add(new_employer)
            db.session.commit()
            flash('Employer added successfully!', 'success')

        return redirect(url_for('add_employer'))

    return render_template('add_employer.html')

@app.route('/add_job_listing', methods=['GET', 'POST'])
def add_job_listing():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        employer_id = request.form['employer_id']

        if title and description and category and employer_id:
            employer = Employer.query.get(employer_id)
            if employer:
                new_job = JobListing(title=title, description=description, category=category, employer_id=employer.id)
                db.session.add(new_job)
                db.session.commit()
                flash('Job listing added successfully!', 'success')
            else:
                flash('Employer not found.', 'error')
        else:
            flash('Please fill in all fields.', 'error')

        return redirect(url_for('add_job_listing'))

    employers = Employer.query.all()
    return render_template('add_job_listing.html', employers=employers)

@app.route('/job_listings', methods=['GET'])
def job_listings():
    title = request.args.get('title')
    category = request.args.get('category')

    query = JobListing.query
    if title:
        query = query.filter(JobListing.title.like(f"%{title}%"))
    if category:
        query = query.filter(JobListing.category == category)

    listings = query.all()
    return render_template('job_listings.html', listings=listings)

@app.route('/delete_job_listing/<int:id>', methods=['POST'])
def delete_job_listing(id):
    job_listing = JobListing.query.get(id)
    if job_listing:
        db.session.delete(job_listing)
        db.session.commit()
        flash('Job listing deleted successfully!', 'success')
        return redirect(url_for('job_listings'))
    flash('Job listing not found.', 'error')
    return redirect(url_for('job_listings'))

@app.route('/candidates')
def candidates():
    candidates = Candidate.query.all()
    return render_template('candidates.html', candidates=candidates)

@app.route('/status_updates')
def status_updates():
    updates = JobStatusUpdate.query.all()
    return render_template('status_updates.html', status_updates=updates)

@app.route('/applications')
def applications():
    applications = Application.query.all()
    return render_template('applications.html', applications=applications)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
