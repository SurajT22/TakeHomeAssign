from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/takehome_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Models
class JobListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_listing_id = db.Column(db.Integer, db.ForeignKey('job_listing.id'), nullable=False)
    candidate_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)


# Pydantic Models
class JobListingSchema(BaseModel):
    title: str
    description: str
    requirements: str
    location: str


class ApplicationSchema(BaseModel):
    job_listing_id: int
    candidate_id: int


# Job Listing Management
@app.route('/job_listings', methods=['POST'])
def create_job_listing():
    data = request.get_json()
    job_listing_schema = JobListingSchema(**data)
    job_listing = JobListing(
        title=job_listing_schema.title,
        description=job_listing_schema.description,
        requirements=job_listing_schema.requirements,
        location=job_listing_schema.location
    )
    db.session.add(job_listing)
    db.session.commit()
    return jsonify({'message': 'Job listing created successfully'})


@app.route('/job_listings/<int:job_id>', methods=['PUT'])
def update_job_listing(job_id):
    job_listing = JobListing.query.get(job_id)
    if not job_listing:
        return jsonify({'error': 'Job listing not found'}), 404

    data = request.get_json()
    job_listing_schema = JobListingSchema(**data)
    job_listing.title = job_listing_schema.title
    job_listing.description = job_listing_schema.description
    job_listing.requirements = job_listing_schema.requirements
    job_listing.location = job_listing_schema.location

    db.session.commit()
    return jsonify({'message': 'Job listing updated successfully'})


# Job Viewing and Application
@app.route('/job_listings', methods=['GET'])
def get_job_listings():
    """Get List of TODO
    '''
        get:
            description: get List of job_listing
            response:
                200:
                    description: Return  a todo list
                    content:
                        application/json:
                            schema:JobListResponseSchema

    :return:
    """
    job_listings = JobListing.query.all()
    job_listings_data = [
        {
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'requirements': job.requirements,
            'location': job.location
        }
        for job in job_listings
    ]
    return jsonify({'job_listings': job_listings_data})



@app.route('/apply', methods=['POST'])
def apply_for_job():
    data = request.get_json()
    application_schema = ApplicationSchema(**data)

    job_listing_id = application_schema.job_listing_id
    candidate_id = application_schema.candidate_id

    # Check if the job listing and candidate exist
    job_listing = JobListing.query.get(job_listing_id)
    if not job_listing:
        return jsonify({'error': 'Job listing not found'}), 404

    # Create the application
    application = Application(
        job_listing_id=job_listing_id,
        candidate_id=candidate_id,
        status='Pending'
    )
    db.session.add(application)
    db.session.commit()

    return jsonify({'message': 'Application submitted successfully'})


# Candidate Application Tracking
@app.route('/candidates/<int:candidate_id>/applications', methods=['GET'])
def get_candidate_applications(candidate_id):
    applications = Application.query.filter_by(candidate_id=candidate_id).all()
    applications_data = [
        {
            'id': app.id,
            'job_listing_id': app.job_listing_id,
            'status': app.status
        }
        for app in applications
    ]
    return jsonify({'applications': applications_data})


# Application Status Tracking
@app.route('/candidates/<int:candidate_id>/applications/<int:application_id>', methods=['GET'])
def get_application_status(candidate_id, application_id):
    application = Application.query.get(application_id)
    if not application or application.candidate_id != candidate_id:
        return jsonify({'error': 'Application not found'}), 404

    return jsonify({'status': application.status})


if __name__ == '__main__':
    app.run(debug=True)
