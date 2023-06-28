import pytest
import unittest
from flask import Flask, jsonify
from main import JobListing, Application, app, db


class FlaskTestCase(unittest.TestCase,pytest):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            # Perform any necessary setup or operations within the application context
            db.create_all()

    def tearDown(self):
        with app.app_context():
            # Perform any necessary cleanup or operations within the application context
            db.drop_all()

    def test_get_job_listings(self):
        with app.app_context():
            # Use the JobListing and Application classes for testing
            # Example:
            job_listings = JobListing.query.all()
        # Assert the expected results
        return job_listings



if __name__ == '__main__':
    unittest.main()

#
# def get_job_listings(unittest.TestCase,**params):
#     defaults = {
#         'id': 1,
#         'title': "Python Developer",
#         'description': "python developer for api creation",
#         'requirements': "Python,api,django,postgress",
#         'location': "Nagpur,Pune"
#     }
#     defaults.update(**params)
#     job_description =JobListing.objects.create(**defaults)
#     return job_description
