# Import necessary libraries and modules
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Import custom modules for database interactions
import usersDB
import projectsDB
import hardwareDB

# Load environment variables
load_dotenv()

# Define the MongoDB connection string
MONGODB_SERVER = os.getenv('MONGODB_SERVER')

# Initialize a new Flask web application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper function to get MongoDB client
def get_mongo_client():
    return MongoClient(MONGODB_SERVER)

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    # Extract data from request
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Attempt to log in the user using the usersDB module
        success = usersDB.login(db, username, password)

        # Return a JSON response
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for the main page (Work in progress)
@app.route('/main')
def mainPage():
    # This route is a work in progress. It could return some basic info or stats.
    return jsonify({"message": "Welcome to the HaaS system main page"})

# Route for joining a project
@app.route('/join_project', methods=['POST'])
def join_project():
    # Extract data from request
    data = request.json
    userId = data.get("userId")
    projectId = data.get("projectId")

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Attempt to join the project using the usersDB module
        success = usersDB.joinProject(db, userId, projectId)

        # Return a JSON response
        return jsonify({"success": True if success else False})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for adding a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    # Extract data from request
    data = request.json
    username = data.get("username")
    userId = data.get("userId")
    password = data.get("password")

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Attempt to add the user using the usersDB module
        success = usersDB.addUser(db, username, userId, password)

        # Return a JSON response
        return jsonify({"success": True if success else False})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for getting the list of user projects
@app.route('/get_user_projects_list', methods=['POST'])
def get_user_projects_list():
    # Extract data from request
    data = request.json
    userId = data.get("userId")

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Fetch the user's projects using the usersDB module
        projects = usersDB.getUserProjectsList(db, userId)

        # Return a JSON response
        return jsonify({"projects": projects})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    # Extract data from request
    data = request.json
    projectName = data.get("projectName")
    projectId = data.get("projectId")
    description = data.get("description")

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Attempt to create the project using the projectsDB module
        success = project