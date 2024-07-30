from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient

# Set up logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
mongo_uri = 'mongodb+srv://atownz1:OneMillion100Beers@onemillion.opehmx7.mongodb.net/haaspoc?retryWrites=true&w=majority&appName=OneMillion'
jwt_secret_key = 'OneMillion100Beers'

app.logger.info(f"MONGO_URI: {mongo_uri}")
app.logger.info(f"JWT_SECRET_KEY is set: {'Yes' if jwt_secret_key else 'No'}")

if not mongo_uri:
    raise ValueError("MONGO_URI is not set. Please check your .env file.")

app.config['MONGO_URI'] = mongo_uri
app.config['JWT_SECRET_KEY'] = jwt_secret_key

# Initialize extensions
mongo = None
try:
    # Use MongoClient directly instead of PyMongo
    client = MongoClient(mongo_uri)
    db = client.get_database('haas_poc')  # Specify the database name here
    # Test the connection
    db.command('ping')
    app.logger.info("MongoDB connection successful")
    mongo = PyMongo(app)
except ConnectionFailure as e:
    app.logger.error(f"MongoDB connection failed: {str(e)}")
    raise
except Exception as e:
    app.logger.error(f"Unexpected error when connecting to MongoDB: {str(e)}")
    raise

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User routes
@app.route('/api/register', methods=['POST'])
def register():
    app.logger.info("Received registration request")
    app.logger.info(f"Request JSON: {request.json}")
    if not mongo or not mongo.db:
        app.logger.error("MongoDB connection is not available")
        return jsonify({'message': 'Database connection error'}), 500
    
    users = mongo.db.users
    username = request.json.get('username')
    password = request.json.get('password')
    
    if users.find_one({'username': username}):
        app.logger.info(f"Username {username} already exists")
        return jsonify({'message': 'Username already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = users.insert_one({'username': username, 'password': hashed_password}).inserted_id
    
    app.logger.info(f"Registered new user: {username}")
    return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)}), 201

@app.route('/api/login', methods=['POST'])
def login():
    app.logger.info("Received login request")
    app.logger.info(f"Request JSON: {request.json}")    
    if not mongo or not mongo.db:
        app.logger.error("MongoDB connection is not available")
        return jsonify({'message': 'Database connection error'}), 500
    
    users = mongo.db.users
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = users.find_one({'username': username})
    
    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=str(user['_id']))
        app.logger.info(f"Login successful for user: {username}")
        return jsonify({'access_token': access_token}), 200
    
    app.logger.info(f"Login failed for user: {username}")
    return jsonify({'message': 'Invalid username or password'}), 401

# Project routes
@app.route('/api/projects', methods=['POST'])
@jwt_required()
def create_project():
    projects = mongo.db.projects
    name = request.json.get('name')
    description = request.json.get('description')
    project_id = request.json.get('projectID')
    user_id = get_jwt_identity()
    
    project = {
        'name': name,
        'description': description,
        'projectID': project_id,
        'user_id': user_id
    }
    
    result = projects.insert_one(project)
    return jsonify({'message': 'Project created successfully', 'project_id': str(result.inserted_id)}), 201

@app.route('/api/projects', methods=['GET'])
@jwt_required()
def get_projects():
    projects = mongo.db.projects
    user_id = get_jwt_identity()
    user_projects = list(projects.find({'user_id': user_id}))
    
    return jsonify([{**project, '_id': str(project['_id'])} for project in user_projects]), 200

# Resource routes
@app.route('/api/resources', methods=['GET'])
@jwt_required()
def get_resources():
    resources = mongo.db.resources
    all_resources = list(resources.find())
    
    return jsonify([{**resource, '_id': str(resource['_id'])} for resource in all_resources]), 200

@app.route('/api/resources/checkout', methods=['POST'])
@jwt_required()
def checkout_resources():
    resources = mongo.db.resources
    hw_set = request.json.get('hw_set')
    quantity = request.json.get('quantity')
    
    resource = resources.find_one({'name': hw_set})
    
    if not resource or resource['available'] < quantity:
        return jsonify({'message': 'Insufficient resources available'}), 400
    
    resources.update_one({'name': hw_set}, {'$inc': {'available': -quantity}})
    return jsonify({'message': 'Resources checked out successfully'}), 200

@app.route('/api/resources/checkin', methods=['POST'])
@jwt_required()
def checkin_resources():
    resources = mongo.db.resources
    hw_set = request.json.get('hw_set')
    quantity = request.json.get('quantity')
    
    resource = resources.find_one({'name': hw_set})
    
    if not resource:
        return jsonify({'message': 'Invalid resource'}), 400
    
    resources.update_one({'name': hw_set}, {'$inc': {'available': quantity}})
    return jsonify({'message': 'Resources checked in successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)