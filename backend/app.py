from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import usersDB
import projectsDB
import hardwareDB

# Define the MongoDB connection string
MONGODB_SERVER = "mongodb+srv://atownz1:OneMillion100Beers@onemillion.opehmx7.mongodb.net/"
client = MongoClient(MONGODB_SERVER)
db = client['OneMillion']

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    userId = data.get("userId")
    password = data.get("password")
    success = usersDB.login(client, username, userId, password)
    return jsonify({"success": success})

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get("username")
    userId = data.get("userId")
    password = data.get("password")
    usersDB.addUser(client, username, userId, password)
    return jsonify({"success": True})

@app.route('/join_project', methods=['POST'])
def join_project():
    data = request.json
    userId = data.get("userId")
    projectId = data.get("projectId")
    usersDB.joinProject(client, userId, projectId)
    return jsonify({"success": True})

@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.json
    projectName = data.get("projectName")
    projectId = data.get("projectId")
    description = data.get("description")
    projectsDB.createProject(client, projectName, projectId, description)
    return jsonify({"success": True})

@app.route('/get_user_projects_list', methods=['POST'])
def get_user_projects_list():
    data = request.json
    userId = data.get("userId")
    projects = usersDB.getUserProjectsList(client, userId)
    return jsonify({"projects": projects})

@app.route('/get_all_hw_names', methods=['GET'])
def get_all_hw_names():
    hw_names = hardwareDB.getAllHwNames(client)
    return jsonify({"hardware_names": hw_names})

@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    data = request.json
    hwSetName = data.get("hwSetName")
    totalQty = data.get("totalQty")
    hardwareDB.createHardwareSet(client, hwSetName, totalQty)
    return jsonify({"success": True})

@app.route('/check_out', methods=['POST'])
def check_out():
    data = request.json
    projectId = data.get("projectId")
    hwSetName = data.get("hwSetName")
    qty = data.get("qty")
    userId = data.get("userId")
    projectsDB.checkOutHW(client, projectId, hwSetName, qty, userId)
    return jsonify({"success": True})

@app.route('/check_in', methods=['POST'])
def check_in():
    data = request.json
    projectId = data.get("projectId")
    hwSetName = data.get("hwSetName")
    qty = data.get("qty")
    userId = data.get("userId")
    projectsDB.checkInHW(client, projectId, hwSetName, qty, userId)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
