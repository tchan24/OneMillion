from flask import Flask, request, jsonify, make_response
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from pymongo.errors import ConnectionFailure, OperationFailure
from pymongo import MongoClient

# Set up logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://onemillionhaas.netlify.app"}}, supports_credentials=True)

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
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

def initialize_resources():
    resources = mongo.db.resources
    if resources.count_documents({}) == 0:
        initial_resources = [
            {"name": "HW Set1", "capacity": 200, "available": 200},
            {"name": "HW Set2", "capacity": 500, "available": 500}
        ]
        resources.insert_many(initial_resources)
        app.logger.info("Initialized default resources")

# Call this function when the app starts
with app.app_context():
    initialize_resources()

# User routes
@app.route('/api/register', methods=['POST'])
def register():
    app.logger.info("Received registration request")
    app.logger.info(f"Request JSON: {request.json}")
    
    try:
        users = mongo.db.users
        username = request.json.get('username')
        password = request.json.get('password')
        
        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400
        
        if users.find_one({'username': username}):
            app.logger.info(f"Username {username} already exists")
            return jsonify({'message': 'Username already exists'}), 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = users.insert_one({'username': username, 'password': hashed_password}).inserted_id
        
        app.logger.info(f"Registered new user: {username}")
        return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)}), 201
    
    except OperationFailure as e:
        app.logger.error(f"Database operation failed: {str(e)}")
        return jsonify({'message': 'Registration failed due to a database error'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error during registration: {str(e)}")
        return jsonify({'message': 'Registration failed due to an unexpected error'}), 500

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "https://onemillionhaas.netlify.app")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    elif request.method == 'POST':
        users = mongo.db.users
        username = request.json.get('username')
        password = request.json.get('password')
        
        user = users.find_one({'username': username})
        
        if user and bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity=str(user['_id']))
            response = jsonify({'access_token': access_token})
            response.headers.add("Access-Control-Allow-Origin", "https://onemillionhaas.netlify.app")
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
        
        response = jsonify({'message': 'Invalid username or password'})
        response.headers.add("Access-Control-Allow-Origin", "https://onemillionhaas.netlify.app")
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 401

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
    resources = mongo.db.resources.find()
    return jsonify([{
        'id': str(resource['_id']),
        'name': resource['name'],
        'capacity': resource['capacity'],
        'available': resource['available']
    } for resource in resources])

@app.route('/api/resources/checkout', methods=['POST'])
@jwt_required()
def checkout_resource():
    data = request.json
    resource = mongo.db.resources.find_one({'name': data['hw_set']})
    if not resource:
        return jsonify({'message': 'Resource not found'}), 404
    if resource['available'] < data['quantity']:
        return jsonify({'message': 'Not enough resources available'}), 400
    
    mongo.db.resources.update_one(
        {'_id': resource['_id']},
        {'$inc': {'available': -data['quantity']}}
    )
    
    # Record the checkout in a separate collection
    mongo.db.checkouts.insert_one({
        'user_id': get_jwt_identity(),
        'resource_id': resource['_id'],
        'project_id': data['project_id'],
        'quantity': data['quantity']
    })
    
    return jsonify({'message': 'Checkout successful'}), 200

@app.route('/api/resources/checkin', methods=['POST'])
@jwt_required()
def checkin_resource():
    data = request.json
    resource = mongo.db.resources.find_one({'name': data['hw_set']})
    if not resource:
        return jsonify({'message': 'Resource not found'}), 404
    
    mongo.db.resources.update_one(
        {'_id': resource['_id']},
        {'$inc': {'available': data['quantity']}}
    )
    
    # Update or remove the checkout record
    mongo.db.checkouts.delete_one({
        'user_id': get_jwt_identity(),
        'resource_id': resource['_id'],
        'project_id': data['project_id'],
        'quantity': data['quantity']
    })
    
    return jsonify({'message': 'Check-in successful'}), 200

@app.route('/api/all-projects', methods=['GET'])
@jwt_required()
def get_all_projects():
    projects = mongo.db.projects
    all_projects = list(projects.find())
    return jsonify([{**project, '_id': str(project['_id'])} for project in all_projects]), 200

@app.route('/api/join-project', methods=['POST'])
@jwt_required()
def join_project():
    user_id = get_jwt_identity()
    project_id = request.json.get('project_id')
    
    project = mongo.db.projects.find_one({'_id': project_id})
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    
    if user_id not in project.get('members', []):
        mongo.db.projects.update_one(
            {'_id': project_id},
            {'$addToSet': {'members': user_id}}
        )
    
    return jsonify({'message': 'Joined project successfully'}), 200

@app.route('/api/projects/<project_id>/resources', methods=['GET'])
@jwt_required()
def get_project_resources(project_id):
    checkouts = mongo.db.checkouts.find({'project_id': project_id})
    project_resources = {}
    for checkout in checkouts:
        resource = mongo.db.resources.find_one({'_id': checkout['resource_id']})
        if resource['name'] not in project_resources:
            project_resources[resource['name']] = 0
        project_resources[resource['name']] += checkout['quantity']
    
    return jsonify([{'name': name, 'checked_out': quantity} for name, quantity in project_resources.items()]), 200

if __name__ == '__main__':
    app.run(debug=False)