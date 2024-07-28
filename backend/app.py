from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Configuration
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/haas_poc'
# app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')

# Configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Initialize extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User routes
@app.route('/api/register', methods=['POST'])
def register():
    users = mongo.db.users
    username = request.json.get('username')
    password = request.json.get('password')
    
    if users.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = users.insert_one({'username': username, 'password': hashed_password}).inserted_id
    
    return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)}), 201

@app.route('/api/login', methods=['POST'])
def login():
    users = mongo.db.users
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = users.find_one({'username': username})
    
    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify({'access_token': access_token}), 200
    
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