from flask import Flask, request, jsonify, session, render_template, url_for
from flask.ext.restful import Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy

#from app import views, models

# Iniatialize the application
app = Flask(__name__)

# Load the Application configuration
app.config.from_object('config.DevelopmentConfigMySQL')

# Load the database
db = SQLAlchemy(app)

# Load the Restful API module
api = Api(app)

# Initialize the Job Properties REST API
from app import myapi

with app.test_request_context():
    print url_for('tags')
    print app.url_map