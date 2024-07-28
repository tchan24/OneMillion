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
        success = projectsDB.createProject(db, projectName, projectId, description)

        # Return a JSON response
        return jsonify({"success": True if success else False})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for getting project information
@app.route('/get_project_info', methods=['POST'])
def get_project_info():
    # Extract data from request
    data = request.json
    projectId = data.get("projectId")

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Fetch project information using the projectsDB module
        project_info = projectsDB.getProjectInfo(db, projectId)

        # Return a JSON response
        return jsonify(project_info)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for getting all hardware names
@app.route('/get_all_hw_names', methods=['GET'])
def get_all_hw_names():
    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Fetch all hardware names using the hardwareDB module
        hw_names = hardwareDB.getAllHwNames(db)

        # Return a JSON response
        return jsonify({"hardware_names": hw_names})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for getting hardware information
@app.route('/get_hw_info', methods=['POST'])
def get_hw_info():
    # Extract data from request
    data = request.json
    hwSetName = data.get("hwSetName")

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Fetch hardware set information using the hardwareDB module
        hw_info = hardwareDB.getHwInfo(db, hwSetName)

        # Return a JSON response
        return jsonify(hw_info)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for checking out hardware
@app.route('/check_out', methods=['POST'])
def check_out():
    # Extract data from request
    data = request.json
    projectId = data.get("projectId")
    hwSetName = data.get("hwSetName")
    qty = data.get("qty")
    userId = data.get("userId")

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Attempt to check out the hardware using the projectsDB module
        success = projectsDB.checkOutHW(db, projectId, hwSetName, qty, userId)

        # Return a JSON response
        return jsonify({"success": True if success else False})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for checking in hardware
@app.route('/check_in', methods=['POST'])
def check_in():
    # Extract data from request
    data = request.json
    projectId = data.get("projectId")
    hwSetName = data.get("hwSetName")
    qty = data.get("qty")
    userId = data.get("userId")

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Attempt to check in the hardware using the projectsDB module
        success = projectsDB.checkInHW(db, projectId, hwSetName, qty, userId)

        # Return a JSON response
        return jsonify({"success": True if success else False})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for creating a new hardware set
@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    # Extract data from request
    data = request.json
    hwSetName = data.get("hwSetName")
    totalQty = data.get("totalQty")

    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Attempt to create the hardware set using the hardwareDB module
        success = hardwareDB.createHardwareSet(db, hwSetName, totalQty)

        # Return a JSON response
        return jsonify({"success": True if success else False})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Route for checking the inventory of projects
@app.route('/api/inventory', methods=['GET'])
def check_inventory():
    # Connect to MongoDB
    client = get_mongo_client()
    db = client['OneMillion']

    try:
        # Fetch all projects from the HardwareCheckout.Projects collection
        projects = list(db.Projects.find({}, {'_id': 0}))

        # Return a JSON response
        return jsonify({"projects": projects})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # Close the MongoDB connection
        client.close()

# Main entry point for the application
if __name__ == '__main__':
    app.run(debug=True)
