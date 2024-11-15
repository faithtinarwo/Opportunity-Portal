import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Database configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{os.getenv('DB_PASSWORD')}@localhost/opportunity_portal"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models definition
class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    job_listings = db.relationship('JobListing', backref='employer', lazy=True)

    def __repr__(self):
        return f'<Employer {self.name}>'

class JobListing(db.Model):
    __tablename__ = 'job_listing'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    expiration_date = db.Column(db.DateTime, default=datetime.now(timezone.utc) + timedelta(days=7))

    def __repr__(self):
        return f'<JobListing {self.title}>'

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    applications = db.relationship('Application', backref='candidate', lazy=True)

    def __repr__(self):
        return f'<Candidate {self.name}>'

class Application(db.Model):
    __tablename__ = 'applications'
    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_listing.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='applied')

    def __repr__(self):
        return f'<Application {self.application_id} for Job {self.job_id}>'

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_employer', methods=['GET', 'POST'])
def add_employer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_employer = Employer(name=name, email=email)
        db.session.add(new_employer)
        db.session.commit()
        return redirect(url_for('job_listings'))  # Redirect to job listings page or any other page
    
    return render_template('add_employer.html')  # Render the employer form

@app.route('/add_job_listing', methods=['GET', 'POST'])
def add_job_listing():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        employer_id = request.form.get('employer_id')
        
        if not employer_id:
            return "Employer ID is missing", 400
        
        new_job_listing = JobListing(title=title, description=description, employer_id=employer_id)
        db.session.add(new_job_listing)
        db.session.commit()
        return redirect(url_for('job_listings'))
    
    employers = Employer.query.all()
    return render_template('add_job_listing.html', employers=employers)

# Route for viewing job listings
@app.route('/job_listings')
def job_listings():
    listings = JobListing.query.all()
    return render_template('job_listings.html', listings=listings)

# Route for deleting a job listing
@app.route('/delete_job_listing/<int:id>', methods=['POST'])
def delete_job_listing(id):
    job_listing = JobListing.query.get(id)
    if job_listing:
        db.session.delete(job_listing)
        db.session.commit()
        return redirect(url_for('job_listings'))
    return "Job listing not found", 404

# Route for candidates
@app.route('/candidates')
def candidates():
    candidates = Candidate.query.all()
    return render_template('candidates.html', candidates=candidates)

# Route for viewing applications
@app.route('/applications')
def applications():
    all_applications = Application.query.all()
    return render_template('applications.html', applications=all_applications)

# Route for searching job listings
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = JobListing.query.filter(JobListing.title.contains(query)).all()
    return render_template('search_results.html', results=results)

# Route for viewing a specific application by ID
@app.route('/applications/<int:id>')
def view_application(id):
    application = Application.query.get(id)
    if application is None:
        return "Application not found", 404
    return render_template('view_application.html', application=application)

# Route for status updates (add this to prevent 404 errors)
@app.route('/status_updates')
def status_updates():
    # Logic to fetch and display status updates (can be customized)
    return render_template('status_updates.html')

# Test the database connection
from sqlalchemy import text
@app.route('/test_connection')
def test_connection():
    try:
        result = db.session.execute(text('SELECT 1'))
        return "Database connection is successful!"
    except Exception as e:
        return f"Database connection failed: {str(e)}"

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
